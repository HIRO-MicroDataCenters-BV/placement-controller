from typing import Any, List

import asyncio

from loguru import logger
from prometheus_async.aio.web import start_http_server

from placement_controller.api.app import start_fastapi
from placement_controller.clients.k8s.client import KubeClient
from placement_controller.core.applications import Applications
from placement_controller.resources.resource_managment import ResourceManagement
from placement_controller.resources.resource_metrics import ResourceMetricsImpl
from placement_controller.resources.resource_tracking import ResourceTrackingImpl
from placement_controller.resources.types import ResourceTracking
from placement_controller.settings import Settings
from placement_controller.util.clock import Clock


class Context:
    loop: asyncio.AbstractEventLoop
    terminated: asyncio.Event
    tasks: List[asyncio.Task[Any]]
    settings: Settings
    applications: Applications
    resource_tracking: ResourceTracking

    def __init__(self, clock: Clock, client: KubeClient, settings: Settings, loop: asyncio.AbstractEventLoop):
        self.settings = settings
        self.terminated = asyncio.Event()
        self.loop = loop
        self.tasks = []
        self.resource_metrics = ResourceMetricsImpl(config=self.settings.metrics)
        self.applications = Applications(clock, client, self.terminated, settings.placement)
        self.resource_tracking = ResourceTrackingImpl(client, self.terminated)
        self.resource_management = ResourceManagement(client, self.resource_tracking, self.resource_metrics)

    def start(self) -> None:
        if self.terminated.is_set():
            return
        self.terminated.clear()
        self.loop.run_until_complete(self.run_tasks())

    async def run_tasks(self) -> None:
        self.tasks.append(self.loop.create_task(self.resource_tracking.start()))
        self.tasks.append(self.loop.create_task(self.applications.run()))
        self.tasks.append(
            self.loop.create_task(start_fastapi(self.settings.api.port, self.applications, self.resource_management))
        )
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
