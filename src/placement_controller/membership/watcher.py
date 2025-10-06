from typing import Optional

import asyncio

from placement_controller.clients.k8s.client import GroupVersionKind, KubeClient
from placement_controller.clients.k8s.event import KubeEvent
from placement_controller.k8s.object_pool import ObjectPool
from placement_controller.membership.types import Membership, MeshPeer, PeerStatus, PlacementZone


class MembershipWatcher(ObjectPool[MeshPeer]):
    MESHPEER_GVK: GroupVersionKind = MeshPeer.GVK
    membership: Optional[Membership]

    def __init__(self, client: KubeClient, is_terminated: asyncio.Event):
        super().__init__(MeshPeer, client, MembershipWatcher.MESHPEER_GVK, is_terminated)
        self.membership = None

    async def handle_event(self, event: KubeEvent) -> None:
        await super().handle_event(event)
        new_membership = self.get_membership()
        if new_membership != self.membership:
            self.membership = new_membership

    def get_membership(self) -> Membership:
        zones = set()
        for peer in self.get_objects():
            instance = peer.get_peer_instance()
            if peer.get_state() == PeerStatus.Ready and instance is not None:
                zones.add(PlacementZone(id=instance.zone))
        return Membership(zones=zones)
