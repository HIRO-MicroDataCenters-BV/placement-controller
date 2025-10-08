from typing import Dict, Optional

import asyncio
from dataclasses import dataclass

from loguru import logger

from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.async_queue import AsyncQueue
from placement_controller.jobs.types import Action, ActionResult, ExecutorContext


@dataclass
class InProgressAction:
    action: Action[ActionResult]
    task: Optional[asyncio.Task[None]] = None


# TODO multiple in progress actions
class JobExecutor:
    incoming: AsyncQueue[Action[ActionResult]]
    outgoing: AsyncQueue[ActionResult]
    in_progress: Dict[NamespacedName, InProgressAction]
    context: ExecutorContext

    def __init__(
        self,
        executor_context: ExecutorContext,
        incoming: AsyncQueue[Action[ActionResult]],
        outgoing: AsyncQueue[ActionResult],
        is_terminated: asyncio.Event,
    ):
        self.incoming = incoming
        self.outgoing = outgoing
        self.in_progress = dict()
        self.is_terminated = is_terminated
        self.context = executor_context

    async def run(self) -> None:
        while not self.is_terminated.is_set():
            action = await self.incoming.get()
            try:
                logger.info(f"received action {action}")
                self.handle_action(action)
            except Exception as e:
                logger.error(f"error while handling action {e}")

    def handle_action(self, action: Action[ActionResult]) -> None:
        name = action.get_application_name()
        inprogress_action = InProgressAction(action=action)
        self.in_progress[name] = inprogress_action
        task = asyncio.create_task(self.run_action(action))
        inprogress_action.task = task

    async def run_action(self, action: Action[ActionResult]) -> None:
        result = await action.run(self.context)
        self.outgoing.put_nowait(result)
