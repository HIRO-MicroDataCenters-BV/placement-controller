from typing import Dict

from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.async_queue import AsyncQueue
from placement_controller.jobs.types import Action


class JobExecutor:
    incoming: AsyncQueue[Action]
    outgoing: AsyncQueue[Action]
    in_progress: Dict[NamespacedName, Action]

    def __init__(self, incoming: AsyncQueue[Action], outgoing: AsyncQueue[Action]):
        self.incoming = incoming
        self.outgoing = outgoing
        self.in_progress = dict()

    async def run(self) -> None:
        pass
