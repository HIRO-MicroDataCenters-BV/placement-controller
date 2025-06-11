from typing import Any, Dict, List, Optional

import asyncio

from pydantic import BaseModel

from app.clients.k8s.client import GroupVersionKind, KubeClient, NamespacedName
from app.clients.k8s.event import EventType, KubeEvent
from app.settings import PlacementSettings


class ApplicationId(BaseModel):
    name: str
    namespace: str

    class Config:
        frozen = True

    @staticmethod
    def from_object(object: Dict[str, Any]) -> "ApplicationId":
        name = object["metadata"]["name"]
        namespace = object["metadata"]["namespace"]
        return ApplicationId(name=name, namespace=namespace)


class Application(BaseModel):
    id: ApplicationId
    placements: Optional[List[str]]

    @staticmethod
    def from_object(object: Dict[str, Any]) -> "Application":
        id = ApplicationId.from_object(object)
        status = object.get("status") or {}
        placements = status.get("placements") or None
        return Application(id=id, placements=placements)


class Applications:
    client: KubeClient
    settings: PlacementSettings
    is_terminated: asyncio.Event
    applications: Dict[ApplicationId, Application]
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
                self.handle_event(event)
            except Exception as e:
                print(f"error while handling event {e}")
        self.client.stop_watch(subscriber_id)

    def handle_event(self, event: KubeEvent) -> None:
        if event.event == EventType.ADDED or event.event == EventType.MODIFIED:
            application = Application.from_object(event.object)
            self.applications[application.id] = application
        elif event.event == EventType.DELETED:
            application = Application.from_object(event.object)
            del self.applications[application.id]
        else:
            raise NotImplementedError(f"Unknown event type {event.event}")

    def list(self) -> List[Application]:
        return list(self.applications.values())

    async def set_placement(self, application_id: ApplicationId, zones: List[str]) -> None:
        name = NamespacedName(application_id.name, application_id.namespace)
        object = await self.client.get(self.gvk, name)
        if not object:
            raise Exception("object not found")
        status = object.get("status")
        if not status:
            raise Exception("status is not available")
        status["placements"] = [{"zone": zone, "node-affinity": None} for zone in zones]
        to_update = {"status": status}
        await self.client.patch_status(self.gvk, name, to_update)
