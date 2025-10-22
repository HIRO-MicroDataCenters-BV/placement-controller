from typing import List, Tuple

from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.store.types import DecisionStore


class FakeDecisionStore(DecisionStore):
    decisions: List[Tuple[NamespacedName, str, List[str], str, str, int]]

    def __init__(self):
        self.decisions = []

    async def save(
        self,
        name: NamespacedName,
        spec: str,
        placement: List[str],
        reason: str,
        trace: str,
        timestamp: int,
    ) -> None:
        self.decisions.append((name, spec, placement, reason, trace, timestamp))
