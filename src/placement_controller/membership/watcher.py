from typing import Callable, Optional

import asyncio

from placement_controller.clients.k8s.client import KubeClient
from placement_controller.clients.k8s.event import KubeEvent
from placement_controller.k8s.object_pool import ObjectPool
from placement_controller.membership.types import Membership, MeshPeer, PeerStatus, PlacementZone


class MembershipWatcher(ObjectPool[MeshPeer]):
    membership: Optional[Membership]
    on_membership_change: Optional[Callable[[Membership], None]]

    def __init__(
        self,
        client: KubeClient,
        is_terminated: asyncio.Event,
        on_membership_change: Optional[Callable[[Membership], None]],
    ):
        super().__init__(MeshPeer, client, MeshPeer.GVK, is_terminated)
        self.membership = None
        self.on_membership_change = on_membership_change

    async def handle_event(self, event: KubeEvent) -> None:
        await super().handle_event(event)
        new_membership = self.get_membership()
        if new_membership != self.membership:
            self.membership = new_membership
            if self.on_membership_change:
                self.on_membership_change(self.membership)

    def get_membership(self) -> Membership:
        zones = set()
        for peer in self.get_objects():
            instance = peer.get_peer_instance()
            if peer.get_state() in [PeerStatus.Ready, PeerStatus.Unknown] and instance is not None:
                zones.add(PlacementZone(id=instance.zone))
        return Membership(zones=zones)
