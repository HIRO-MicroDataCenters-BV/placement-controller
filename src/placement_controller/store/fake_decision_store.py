from typing import Any, List

from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.store.types import DecisionStore


class FakeDecisionStore(DecisionStore):
    decisions: List[Any]

    def __init__(self):
        self.decisions = []

    async def save(
        self,
        name: NamespacedName,
        placement: List[str],
        reason: str,
        trace: str,
        timestamp: int,
    ) -> None:
        pass
