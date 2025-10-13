from typing import Any, Dict, Optional, Set

from dataclasses import dataclass
from enum import StrEnum

from placement_controller.clients.k8s.client import GroupVersionKind
from placement_controller.clients.k8s.resource import BaseResource

ZoneId = str


@dataclass(frozen=True)
class PlacementZone:
    id: ZoneId


@dataclass
class Membership:
    zones: Set[PlacementZone]


class PeerStatus(StrEnum):
    Ready = "Ready"
    NotReady = "NotReady"
    Unavailable = "Unavailable"


@dataclass
class MeshPeerInstance:
    zone: str
    start_time: str
    start_timestamp: int


class MeshPeer(BaseResource):
    GVK: GroupVersionKind = GroupVersionKind("dcp.hiro.io", "v1", "MeshPeer")

    def __init__(self, object: Dict[str, Any]):
        super().__init__(object)

    def get_name(self) -> str:
        return self.object["metadata"]["name"]  # type: ignore

    def get_state(self) -> PeerStatus:
        status = self.object.get("status") or {}
        peer_status = status.get("status") or "Unavailable"
        return PeerStatus(peer_status)

    def get_peer_instance(self) -> Optional[MeshPeerInstance]:
        status = self.object.get("status") or {}
        instance_dict = status.get("instance")
        if instance_dict:
            return MeshPeerInstance(
                zone=instance_dict["zone"],
                start_time=instance_dict["start_time"],
                start_timestamp=instance_dict["start_timestamp"],
            )
        else:
            return None
