from typing import Any, List

import asyncio

from application_client.client import Client
from loguru import logger
from prometheus_async.aio.web import start_http_server

from placement_controller.api.app import start_fastapi
from placement_controller.clients.k8s.client import KubeClient
from placement_controller.clients.placement.local import LocalPlacementClient
from placement_controller.core.applications import Applications
from placement_controller.jobs.types import ExecutorContext
from placement_controller.resources.resource_managment import ResourceManagementImpl
from placement_controller.resources.resource_metrics import ResourceMetricsImpl
from placement_controller.resources.resource_tracking import ResourceTrackingImpl
from placement_controller.settings import Settings
from placement_controller.util.clock import Clock
from placement_controller.zone.zone_api_factory import ZoneApiFactoryImpl


class Context:
    loop: asyncio.AbstractEventLoop
    terminated: asyncio.Event
    tasks: List[asyncio.Task[Any]]
    settings: Settings

    resource_metrics: ResourceMetricsImpl
    resource_tracking: ResourceTrackingImpl
    resource_management: ResourceManagementImpl
    executor_context: ExecutorContext
    applications: Applications

    def __init__(
        self,
        clock: Clock,
        app_client: Client,
        zone_api_factory: ZoneApiFactoryImpl,
        kube_client: KubeClient,
        settings: Settings,
        loop: asyncio.AbstractEventLoop,
    ):
        self.settings = settings
        self.terminated = asyncio.Event()
        self.loop = loop
        self.tasks = []
        self.resource_metrics = ResourceMetricsImpl(config=self.settings.metrics)
        self.resource_tracking = ResourceTrackingImpl(kube_client, self.terminated)
        self.resource_management = ResourceManagementImpl(kube_client, self.resource_tracking, self.resource_metrics)
        zone_api_factory.set_local_client(LocalPlacementClient(self.resource_management))

        self.executor_context = ExecutorContext(
            application_controller_client=app_client,
            zone_api_factory=zone_api_factory,
            kube_client=kube_client,
            clock=clock,
        )

        self.applications = Applications(clock, self.executor_context, kube_client, self.terminated, settings.placement)

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
