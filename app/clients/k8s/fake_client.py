from typing import Any, Dict, List, Optional, Tuple, override

import copy
from dataclasses import dataclass

from app.clients.k8s.client import GroupVersionKind, KubeClient, NamespacedName, SubscriberId
from app.clients.k8s.event import EventType, KubeEvent
from app.core.async_queue import AsyncQueue


@dataclass
class Subscription:
    gvk: GroupVersionKind
    namespace: str
    queue: AsyncQueue[KubeEvent]


class FakeClient(KubeClient):
    objects: Dict[GroupVersionKind, Dict[NamespacedName, Dict[str, Any]]]
    subscriptions: Dict[SubscriberId, Subscription]
    events: List[KubeEvent]
    versions: int
    subscriber_ids: SubscriberId
    uids: int

    def __init__(self):
        self.objects = {}
        self.subscriptions = {}
        self.events = []
        self.versions = 0
        self.uids = 0
        self.subscriber_ids = 0

    @override
    def watch(
        self,
        gvk: GroupVersionKind,
        namespace: Optional[str],
        version_since: int,
        timeout_seconds: int,
    ) -> Tuple[SubscriberId, AsyncQueue[KubeEvent]]:
        queue = AsyncQueue[KubeEvent]()
        subscription = Subscription(gvk=gvk, queue=queue, namespace=namespace or "default")
        self.subscriber_ids += 1
        self.subscriptions[self.subscriber_ids] = subscription
        return self.subscriber_ids, queue

    @override
    def stop_watch(self, subscriber_id: SubscriberId) -> None:
        del self.subscriptions[subscriber_id]

    @override
    async def patch(self, gvk: GroupVersionKind, object: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        object = copy.deepcopy(object)
        self.ensure_version(object)

        named_objects = self.objects.setdefault(gvk, {})
        name = NamespacedName.get_name(object)
        if name in named_objects:
            event_type = EventType.MODIFIED
        else:
            event_type = EventType.ADDED
        named_objects[name] = object

        self.send_event(KubeEvent(event=event_type, version=int(object["metadata"]["resourceVersion"]), object=object))

        return object

    @override
    async def patch_status(
        self, gvk: GroupVersionKind, name: NamespacedName, status: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        named_objects = self.objects.get(gvk)
        if not named_objects:
            return None

        current = named_objects.get(name)
        if not current:
            return None
        current = copy.deepcopy(current)
        current["status"] = status["status"]
        self.ensure_version(current)
        named_objects[name] = current

        self.send_event(
            KubeEvent(event=EventType.MODIFIED, version=int(current["metadata"]["resourceVersion"]), object=current)
        )
        return current

    @override
    async def get(self, gvk: GroupVersionKind, name: NamespacedName) -> Optional[Dict[str, Any]]:
        named_objects = self.objects.get(gvk)
        if not named_objects:
            return None
        object = named_objects.get(name)
        if not object:
            return None
        else:
            return copy.deepcopy(object)

    @override
    async def delete(self, gvk: GroupVersionKind, name: NamespacedName) -> Optional[Dict[str, Any]]:
        named_objects = self.objects.get(gvk)
        if not named_objects:
            return None
        object = named_objects.get(name)
        if object:
            del named_objects[name]
            object = copy.deepcopy(object)
            self.ensure_version(object)
            self.send_event(
                KubeEvent(event=EventType.DELETED, version=int(object["metadata"]["resourceVersion"]), object=object)
            )
            return object
        else:
            return None

    def ensure_version(self, object: Dict[str, Any]) -> None:
        self.versions += 1
        object["metadata"]["resourceVersion"] = str(self.versions)
        if "uid" not in object["metadata"]:
            self.uids += 1
            object["metadata"]["uid"] = str(self.uids)

    def send_event(self, event: KubeEvent) -> None:
        self.events.append(event)
        for _, subscription in self.subscriptions.items():
            namespace = event.object["metadata"]["namespace"]
            if subscription.namespace == namespace:
                subscription.queue.put_nowait(event)
