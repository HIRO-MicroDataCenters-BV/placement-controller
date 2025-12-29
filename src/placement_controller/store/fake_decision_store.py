from typing import List

from loguru import logger

from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.resources.trace_log import TraceLogRow
from placement_controller.store.types import DecisionStore


class FakeDecisionStore(DecisionStore):
    decisions: List[TraceLogRow]

    def __init__(self):
        self.decisions = []

    async def save(
        self,
        name: NamespacedName,
        spec: str,
        placement: List[str],
        reason: str,
        trace: List[TraceLogRow],
        timestamp: int,
    ) -> None:
        logger.info(
            f"{name}: Saving decision. placements={placement}, reason='{reason}',"
            + f" trace='{trace}', timestamp={timestamp}",
        )
        self.decisions.extend(trace)
