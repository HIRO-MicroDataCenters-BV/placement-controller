from typing import Any, Dict, Optional, Tuple

from dataclasses import dataclass

from app.clients.k8s.k8s_event import K8SEvent
from app.core.async_queue import AsyncQueue

type SubscriberId = int


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


class K8SClient:
    def watch(
        self,
        gvk: GroupVersionKind,
        namespace: Optional[str],
        version_since: str,
        timeout_seconds: int,
    ) -> Tuple[SubscriberId, AsyncQueue[K8SEvent]]:
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
