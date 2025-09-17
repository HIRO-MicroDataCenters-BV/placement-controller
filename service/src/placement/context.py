from typing import Any, List

import asyncio

from loguru import logger
from prometheus_async.aio.web import start_http_server

from placement.api.app import start_fastapi
from placement.clients.k8s.client import KubeClient
from placement.core.applications import Applications
from placement.settings import Settings
from placement.util.clock import Clock


class Context:
    loop: asyncio.AbstractEventLoop
    terminated: asyncio.Event
    tasks: List[asyncio.Task[Any]]
    settings: Settings
    applications: Applications

    def __init__(self, clock: Clock, client: KubeClient, settings: Settings, loop: asyncio.AbstractEventLoop):
        self.settings = settings
        self.terminated = asyncio.Event()
        self.loop = loop
        self.tasks = []
        self.applications = Applications(client, self.terminated, settings.placement)

    def start(self) -> None:
        if self.terminated.is_set():
            return
        self.terminated.clear()
        self.loop.run_until_complete(self.run_tasks())

    async def run_tasks(self) -> None:
        self.tasks.append(self.loop.create_task(self.applications.run()))
        self.tasks.append(self.loop.create_task(start_fastapi(self.settings.api.port, self.applications)))
        self.prometheus_server = await start_http_server(port=self.settings.prometheus.endpoint_port)

    def stop(self) -> None:
        self.terminated.set()
        for task in self.tasks:
            task.cancel()
        self.loop.run_until_complete(self.prometheus_server.close())

    def wait_for_termination(self) -> None:
        self.loop.run_until_complete(self.terminated.wait())
        logger.info("Application terminated.")

    def exit_gracefully(self, _1: Any, _2: Any) -> None:
        self.stop()
        self.wait_for_termination()
