from typing import List

from orchestrationlib_client.client import Client

from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.store.types import DecisionStore


class DecisionStoreImpl(DecisionStore):
    client: Client

    def __init__(self, client: Client):
        self.client = client

    async def save(
        self,
        name: NamespacedName,
        placement: List[str],
        reason: str,
        trace: str,
        timestamp: int,
    ) -> None:
        pass
        # self.client.
