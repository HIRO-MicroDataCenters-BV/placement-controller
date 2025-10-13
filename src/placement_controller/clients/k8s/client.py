from typing import Any, Dict, List, Optional, Tuple

import asyncio
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from kubernetes_asyncio import client

from placement_controller.clients.k8s.event import KubeEvent
from placement_controller.core.async_queue import AsyncQueue

SubscriberId = int


@dataclass(frozen=True, eq=True)
class NamespacedName:
    name: str
    namespace: str

    @staticmethod
    def get_name(object: Dict[str, Any]) -> "NamespacedName":
        name = object["metadata"]["name"]
        namespace = object["metadata"].get("namespace") or "default"
        return NamespacedName(name, namespace)

    def to_string(self) -> str:
        return f"{self.namespace}/{self.name}"


@dataclass(frozen=True, eq=True)
class GroupVersionKind:
    group: str
    version: str
    kind: str

    @staticmethod
    def from_event(event: KubeEvent) -> "GroupVersionKind":
        groupVersion = event.object["apiVersion"]
        tokens = groupVersion.split("/")
        if len(tokens) != 2:
            group = ""
            version = groupVersion
        else:
            group, version = tokens[0], tokens[1]
        return GroupVersionKind(group, version, event.object["kind"])


class KubeClient:
    def watch(
        self, gvk: GroupVersionKind, namespace: Optional[str], version_since: int, is_terminated: asyncio.Event
    ) -> Tuple[SubscriberId, AsyncQueue[KubeEvent]]:
        raise NotImplementedError

    def stop_watch(self, subscriber_id: SubscriberId) -> None:
        raise NotImplementedError

    async def patch(self, gvk: GroupVersionKind, object: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

    async def patch_status(
        self, gvk: GroupVersionKind, name: NamespacedName, status: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

    async def get(self, gvk: GroupVersionKind, name: NamespacedName) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

    async def list(self, gvk: GroupVersionKind) -> List[Dict[str, Any]]:
        raise NotImplementedError

    async def delete(self, gvk: GroupVersionKind, name: NamespacedName) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

    async def emit_event(
        self,
        gvk: GroupVersionKind,
        name: NamespacedName,
        uid: str,
        reason: str,
        action: str,
        message: str,
        event_type: str,
        timestamp: int,
    ) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

    @staticmethod
    def new_event(
        gvk: GroupVersionKind,
        name: NamespacedName,
        uid: str,
        reason: str,
        action: str,
        message: str,
        event_type: str,
        timestamp: int,
    ) -> client.CoreV1Event:
        dt = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        event_time = dt.isoformat(timespec="microseconds").replace("+00:00", "Z")
        return client.EventsV1Event(
            metadata=client.V1ObjectMeta(name=f"{name.name}-{uuid.uuid4()}", namespace=name.namespace),
            regarding=client.V1ObjectReference(
                api_version=f"{gvk.group}/{gvk.version}",
                kind=gvk.kind,
                name=name.name,
                namespace=name.namespace,
                uid=uid,
            ),
            action=action,
            reason=reason,
            note=message,
            type=event_type,
            event_time=event_time,
            reporting_controller="placement-controller",
            reporting_instance="placement-controller",  # TODO pod_id
        )
