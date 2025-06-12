from typing import Dict, List

import asyncio

from loguru import logger

from app.clients.k8s.client import GroupVersionKind, KubeClient, NamespacedName
from app.clients.k8s.event import EventType, KubeEvent
from app.core.application import Application
from app.settings import PlacementSettings


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

    async def run(self) -> None:
        subscriber_id, queue = self.client.watch(
            self.gvk, self.settings.namespace, version_since=0, timeout_seconds=86400
        )
        while not self.is_terminated.is_set():
            event = await queue.get()
            try:
                logger.info(f"incoming event {event.event}")
                self.handle_event(event)
            except Exception as e:
                logger.error(f"error while handling event {e}")
        self.client.stop_watch(subscriber_id)

    def handle_event(self, event: KubeEvent) -> None:
        if event.event == EventType.ADDED or event.event == EventType.MODIFIED:
            application = Application(event.object)
            self.applications[application.get_namespaced_name()] = application
            self.set_default_placement(application)
        elif event.event == EventType.DELETED:
            application = Application(event.object)
            del self.applications[application.get_namespaced_name()]
        else:
            raise NotImplementedError(f"Unknown event type {event.event}")

    def list(self) -> List[Application]:
        return list(self.applications.values())

    async def set_placement(self, name: NamespacedName, zones: List[str]) -> Application:
        object = await self.client.get(self.gvk, name)
        if not object:
            raise Exception("object not found")

        application = Application(object)
        application.set_placement_zones(zones)

        updated = await self.client.patch_status(self.gvk, name, application.get_status_or_fail())
        if not updated:
            raise Exception("updated object is not available")
        return Application(updated)

    def set_default_placement(self, application: Application) -> None:
        if application.get_status() and application.get_owner_zone() == self.settings.current_zone:
            if len(application.get_placement_zones()) == 0:
                application.set_placement_zones([self.settings.current_zone])
