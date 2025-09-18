from typing import Callable, Dict, List

import asyncio

from loguru import logger

from placement_controller.clients.k8s.client import GroupVersionKind, KubeClient, NamespacedName
from placement_controller.clients.k8s.event import EventType, KubeEvent
from placement_controller.core.application import Application
from placement_controller.settings import PlacementSettings

ApplicationFnMut = Callable[[Application], None]


class Applications:
    client: KubeClient
    settings: PlacementSettings
    is_terminated: asyncio.Event
    applications: Dict[NamespacedName, Application]
    gvk: GroupVersionKind

    def __init__(self, client: KubeClient, is_terminated: asyncio.Event, settings: PlacementSettings):
        self.client = client
        self.settings = settings
        self.is_terminated = is_terminated
        self.applications = {}
        self.gvk = GroupVersionKind(group="dcp.hiro.io", version="v1", kind="AnyApplication")

        logger.info(f"owner zone '{settings.current_zone}'")

    async def run(self) -> None:
        subscriber_id, queue = self.client.watch(self.gvk, self.settings.namespace, 0, self.is_terminated)
        while not self.is_terminated.is_set():
            event = await queue.get()
            try:
                logger.info(f"incoming event {event.event}")
                await self.handle_event(event)
            except Exception as e:
                logger.error(f"error while handling event {e}")
        self.client.stop_watch(subscriber_id)

    async def handle_event(self, event: KubeEvent) -> None:
        if event.event == EventType.ADDED or event.event == EventType.MODIFIED:
            application = Application(event.object)
            self.applications[application.get_namespaced_name()] = application
            await self.set_default_placement(application)
        elif event.event == EventType.DELETED:
            application = Application(event.object)
            del self.applications[application.get_namespaced_name()]
        else:
            raise NotImplementedError(f"Unknown event type {event.event}")

    def list(self) -> List[Application]:
        return list(self.applications.values())

    async def set_default_placement(self, application: Application) -> None:
        if application.get_owner_zone() == self.settings.current_zone:
            if application.get_global_state() == "Placement":
                spec = application.get_spec()
                strategy = spec.get("placementStrategy") or {}
                if strategy.get("strategy") == "Global":
                    # setting default placement zone to current
                    if len(application.get_placement_zones()) == 0:
                        zones = [self.settings.current_zone]
                        name = application.get_namespaced_name()
                        application.set_placement_zones(zones)
                        await self.client.patch_status(self.gvk, name, application.get_status_or_fail())
                        logger.info(f"{name} setting placement zones {zones}")

    async def set_placement(self, name: NamespacedName, zones: List[str]) -> Application:
        return await self.patch_status(name, lambda app: app.set_placement_zones(zones))

    async def set_owner(self, name: NamespacedName, owner: str) -> Application:
        return await self.patch_status(name, lambda app: app.set_owner_zone(owner))

    async def patch_status(self, name: NamespacedName, update_function: ApplicationFnMut) -> Application:
        object = await self.client.get(self.gvk, name)
        if not object:
            raise Exception("object not found")

        application = Application(object)
        update_function(application)

        updated = await self.client.patch_status(self.gvk, name, application.get_status_or_fail())
        if not updated:
            raise Exception("updated object is not available")
        return Application(updated)
