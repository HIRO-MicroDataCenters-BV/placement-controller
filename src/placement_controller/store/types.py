from typing import List

from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.resources.trace_log import TraceLogRow


class DecisionStore:

    async def save(
        self,
        name: NamespacedName,
        spec: str,
        placement: List[str],
        reason: str,
        trace: List[TraceLogRow],
        timestamp: int,
    ) -> None:
        raise NotImplementedError
