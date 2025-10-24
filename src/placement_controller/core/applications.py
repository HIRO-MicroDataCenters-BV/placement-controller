from typing import Callable, List

import asyncio

from loguru import logger

from placement_controller.api.model import ApplicationState
from placement_controller.clients.k8s.client import KubeClient, NamespacedName
from placement_controller.clients.k8s.event import EventType, KubeEvent
from placement_controller.core.application import AnyApplication
from placement_controller.core.async_queue import AsyncQueue
from placement_controller.core.scheduling_queue import SchedulingQueue
from placement_controller.jobs.executor import JobExecutor
from placement_controller.jobs.types import Action, ActionResult, ExecutorContext
from placement_controller.membership.types import Membership, PlacementZone
from placement_controller.membership.watcher import MembershipWatcher
from placement_controller.settings import PlacementSettings
from placement_controller.util.clock import Clock

ApplicationFnMut = Callable[[AnyApplication], None]


class Applications:
    clock: Clock
    client: KubeClient
    settings: PlacementSettings
    is_terminated: asyncio.Event
    membership_watcher: MembershipWatcher
    tick_interval_seconds: float
    initialized: bool

    scheduling_queue: SchedulingQueue
    actions: AsyncQueue[Action[ActionResult]]
    results: AsyncQueue[ActionResult]

    def __init__(
        self,
        clock: Clock,
        executor_context: ExecutorContext,
        client: KubeClient,
        is_terminated: asyncio.Event,
        settings: PlacementSettings,
    ):
        self.clock = clock
        self.client = client
        self.settings = settings
        self.tick_interval_seconds = 1.0
        self.is_terminated = is_terminated
        self.initialized = False

        self.actions = AsyncQueue[Action[ActionResult]]()
        self.results = AsyncQueue[ActionResult]()
        self.scheduling_queue = SchedulingQueue(clock, settings.current_zone)
        self.membership_watcher = MembershipWatcher(client, self.is_terminated, self.on_membership_change)
        self.executor = JobExecutor(executor_context, self.actions, self.results, self.is_terminated)

        logger.info(f"owner zone '{settings.current_zone}'")
        # this needs to be loaded separately from kubernetes on boot

        self.scheduling_queue.on_membership_update(
            Membership({PlacementZone(id=zone) for zone in self.settings.available_zones}),
            self.clock.now_seconds(),
        )

    def is_initialized(self) -> bool:
        return self.initialized

    async def run(self) -> None:
        await asyncio.gather(
            self.run_kube_watch(),
            self.run_result_listener(),
            self.executor.run(),
            self.membership_watcher.start(),
            self.ticker(),
        )

    async def run_kube_watch(self) -> None:
        subscriber_id, queue = self.client.watch(AnyApplication.GVK, self.settings.namespace, 0, self.is_terminated)
        self.initialized = True
        while not self.is_terminated.is_set():
            event = await queue.get()
            try:
                logger.info(f"{AnyApplication.GVK.to_string()} incoming event {event.event}")
                await self.handle_event(event)
            except Exception as e:
                logger.error(f"{AnyApplication.GVK.to_string()} error while handling event {e}")
        self.client.stop_watch(subscriber_id)

    async def handle_event(self, event: KubeEvent) -> None:
        if event.event == EventType.SNAPSHOT:
            if not isinstance(event.object, list):
                logger.warning(f"{AnyApplication.GVK.to_string()} Skipping Snapshot event. List expected.")
                return

            applications = [AnyApplication(event_object) for event_object in event.object]
            action_result = self.scheduling_queue.load_state(applications)
            self.handle_actions(action_result)

        elif event.event == EventType.ADDED or event.event == EventType.MODIFIED:
            if not isinstance(event.object, dict):
                logger.warning(f"{AnyApplication.GVK.to_string()} Skipping Update event. Dict expected.")
                return

            application = AnyApplication(event.object)
            action_result = self.scheduling_queue.on_application_update(application, self.clock.now_seconds())
            self.handle_actions(action_result)

        elif event.event == EventType.DELETED:
            if not isinstance(event.object, dict):
                logger.warning(f"{AnyApplication.GVK.to_string()} Skipping Update event. Dict expected.")
                return

            application = AnyApplication(event.object)
            action_result = self.scheduling_queue.on_application_delete(application, self.clock.now_seconds())
            self.handle_actions(action_result)

        else:
            raise NotImplementedError(f"{AnyApplication.GVK.to_string()} Unknown event type {event.event}")

    async def run_result_listener(self) -> None:
        logger.info("JobExecutor result listener started.")
        while not self.is_terminated.is_set():
            action_result = await self.results.get()
            try:
                logger.info(
                    f"{action_result.get_application_name().to_string()}: action result {type(action_result).__name__}"
                )
                self.handle_result(action_result)
            except Exception as e:
                logger.error(f"error while handling result {e}")

    def handle_result(self, result: ActionResult) -> None:
        actions = self.scheduling_queue.on_action_result(result, self.clock.now_seconds())
        self.handle_actions(actions)

    def on_membership_change(self, membership: Membership) -> None:
        actions = self.scheduling_queue.on_membership_update(membership, self.clock.now_seconds())
        self.handle_actions(actions)

    async def ticker(self) -> None:
        logger.info("Ticker started.")
        while not self.is_terminated.is_set():
            actions = self.scheduling_queue.on_tick(self.clock.now_seconds())
            self.handle_actions(actions)
            await asyncio.sleep(self.tick_interval_seconds)

    async def list(self) -> List[AnyApplication]:
        applications = await self.client.list(AnyApplication.GVK)
        return [AnyApplication(app) for app in applications]

    def list_scheduling_state(self) -> List[ApplicationState]:
        return self.scheduling_queue.get_scheduling_states()

    async def set_placement(self, name: NamespacedName, zones: List[str]) -> AnyApplication:
        return await self.patch_status(name, lambda app: app.set_placement_zones(zones))

    async def set_owner(self, name: NamespacedName, owner: str) -> AnyApplication:
        return await self.patch_status(name, lambda app: app.set_owner_zone(owner))

    async def patch_status(self, name: NamespacedName, update_function: ApplicationFnMut) -> AnyApplication:
        object = await self.client.get(AnyApplication.GVK, name)
        if not object:
            raise Exception("object not found")

        application = AnyApplication(object)
        update_function(application)

        updated = await self.client.patch_status(AnyApplication.GVK, name, application.get_status_or_fail())
        if not updated:
            raise Exception("updated object is not available")
        return AnyApplication(updated)

    def handle_actions(self, actions: List[Action[ActionResult]]) -> None:
        for action in actions:
            self.actions.put_nowait(action)
