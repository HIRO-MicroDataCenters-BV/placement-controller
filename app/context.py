from typing import Any, List

import asyncio

from loguru import logger
from prometheus_async.aio.web import start_http_server

from app.clients.k8s.k8s_client import K8SClient
from app.settings import Settings
from app.util.clock import Clock


class Context:
    runner: asyncio.Runner
    terminated: asyncio.Event
    tasks: List[asyncio.Task[Any]]
    settings: Settings

    def __init__(
        self,
        clock: Clock,
        k8s_client: K8SClient,
        settings: Settings,
    ):
        self.settings = settings
        self.terminated = asyncio.Event()
        self.runner = asyncio.Runner()
        self.tasks = []

    def start(self) -> None:
        if self.terminated.is_set():
            return
        self.terminated.clear()
        self.runner.run(self.run_tasks())

    async def run_tasks(self) -> None:
        # self.tasks.append(asyncio.create_task(self.k8s_pool.run()))
        self.prometheus_server = await start_http_server(port=self.settings.prometheus.endpoint_port)

    def stop(self) -> None:
        self.terminated.set()
        self.runner.run(self.prometheus_server.close())
        for task in self.tasks:
            task.cancel()

    def wait_for_termination(self) -> None:
        self.runner.run(self.terminated.wait())
        logger.info("Application terminated.")

    def exit_gracefully(self, _1: Any, _2: Any) -> None:
        self.stop()
        self.wait_for_termination()
