from typing import Any, Dict, Optional, Tuple

import asyncio
from dataclasses import dataclass

from placement.clients.k8s.event import KubeEvent
from placement.core.async_queue import AsyncQueue

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


@dataclass(frozen=True, eq=True)
class GroupVersionKind:
    group: str
    version: str
    kind: str


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

    async def delete(self, gvk: GroupVersionKind, name: NamespacedName) -> Optional[Dict[str, Any]]:
        raise NotImplementedError
