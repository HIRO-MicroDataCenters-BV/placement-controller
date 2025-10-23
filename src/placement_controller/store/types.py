from typing import List

from placement_controller.clients.k8s.client import NamespacedName


class DecisionStore:

    async def save(
        self,
        name: NamespacedName,
        spec: str,
        placement: List[str],
        reason: str,
        trace: str,
        timestamp: int,
    ) -> None:
        raise NotImplementedError
