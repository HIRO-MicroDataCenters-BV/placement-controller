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
    initialized: bool

    def __init__(self, cls: Type[T], client: KubeClient, gvk: GroupVersionKind, is_terminated: asyncio.Event):
        self.cls = cls
        self.client = client
        self.gvk = gvk
        self.is_terminated = is_terminated
        self.pool = dict()
        self.active = False
        self.initialized = False

    async def start(self) -> None:
        subscriber_id, queue = self.client.watch(self.gvk, None, 0, self.is_terminated)
        self.active = True
        logger.info(f"ObjectPool{{{self.gvk.to_string()}}} started.")
        while not self.is_terminated.is_set():
            event = await queue.get()
            try:
                logger.info(f"ObjectPool{{{self.gvk.to_string()}}} incoming event {event.event}")
                await self.handle_event(event)
            except Exception as e:
                logger.error(f"ObjectPool{{{self.gvk.to_string()}}} error while handling event {e}")
        self.client.stop_watch(subscriber_id)

    async def handle_event(self, event: KubeEvent) -> None:
        if event.event == EventType.SNAPSHOT:
            if not self.initialized:
                if not isinstance(event.object, list):
                    logger.warning(f"ObjectPool{{{self.gvk.to_string()}}} Skipping snapshot event. List expected.")
                    return
                for event_object in event.object:
                    object = self.cls(event_object)
                    self.pool[object.get_namespaced_name()] = object
                logger.info(f"ObjectPool{{{self.gvk.to_string()}}} initialized.")
            self.initialized = True
        elif event.event == EventType.ADDED or event.event == EventType.MODIFIED:
            if not isinstance(event.object, dict):
                logger.warning(f"ObjectPool{{{self.gvk.to_string()}}} Skipping Update event. Dict expected.")
                return
            object = self.cls(event.object)
            self.pool[object.get_namespaced_name()] = object
        elif event.event == EventType.DELETED:
            if not isinstance(event.object, dict):
                logger.warning(f"ObjectPool{{{self.gvk.to_string()}}} Skipping Delete event. Dict expected.")
                return
            object = self.cls(event.object)
            del self.pool[object.get_namespaced_name()]
        else:
            raise NotImplementedError(f"ObjectPool{{{self.gvk.to_string()}}} Unknown event type {event.event}")

    def get_objects(self) -> List[T]:
        return list(self.pool.values())

    def is_subscription_active(self) -> bool:
        return self.active
