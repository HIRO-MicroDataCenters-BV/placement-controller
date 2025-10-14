from typing import Dict, Generic, List, Type, TypeVar

import asyncio

from loguru import logger

from placement_controller.clients.k8s.client import GroupVersionKind, KubeClient, NamespacedName
from placement_controller.clients.k8s.event import EventType, KubeEvent
from placement_controller.clients.k8s.resource import BaseResource

T = TypeVar("T", bound="BaseResource")


class ObjectPool(Generic[T]):

    client: KubeClient
    gvk: GroupVersionKind
    is_terminated: asyncio.Event
    pool: Dict[NamespacedName, T]
    cls: type[T]
    active: bool

    def __init__(self, cls: Type[T], client: KubeClient, gvk: GroupVersionKind, is_terminated: asyncio.Event):
        self.cls = cls
        self.client = client
        self.gvk = gvk
        self.is_terminated = is_terminated
        self.pool = dict()
        self.active = False

    async def start(self) -> None:
        subscriber_id, queue = self.client.watch(self.gvk, None, 0, self.is_terminated)
        self.active = True
        logger.info(f"ObjectPool{{{self.cls}}} started.")
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
            object = self.cls(event.object)
            self.pool[object.get_namespaced_name()] = object
        elif event.event == EventType.DELETED:
            object = self.cls(event.object)
            del self.pool[object.get_namespaced_name()]
        else:
            raise NotImplementedError(f"Unknown event type {event.event}")

    def get_objects(self) -> List[T]:
        return list(self.pool.values())

    def is_subscription_active(self) -> bool:
        return self.active
