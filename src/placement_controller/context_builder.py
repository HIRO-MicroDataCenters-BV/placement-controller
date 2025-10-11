from typing import List, Optional, Tuple

import argparse
import asyncio
from argparse import Namespace
from io import StringIO

from application_client.client import Client

from placement_controller.clients.k8s.client_impl import KubeClientImpl
from placement_controller.context import Context
from placement_controller.jobs.types import ExecutorContext
from placement_controller.pydantic_yaml import from_yaml
from placement_controller.settings import Settings
from placement_controller.util.clock_impl import ClockImpl
from placement_controller.zone.zone_api_factory import ZoneApiFactoryImpl


class ContextBuilder:
    settings: Settings

    def __init__(self, settings: Settings):
        self.settings = settings

    @staticmethod
    def from_args(args: List[str]) -> Optional["ContextBuilder"]:
        is_success, config_or_msg = ContextBuilder.parse_args(args)
        if is_success:
            settings: Settings = from_yaml(config_or_msg, Settings)  # type: ignore
            return ContextBuilder(settings)
        else:
            print(config_or_msg)
            return None

    @staticmethod
    def parse_args(args: List[str]) -> Tuple[bool, str]:
        parser = argparse.ArgumentParser(
            description="Rudimentary placement controller for Decentralized Control Plane.",
            exit_on_error=False,
        )
        parser.add_argument(
            "--config",
            dest="config",
            action="store",
            help="Placement Controller Configuration",
            required=True,
        )

        try:
            ns: Namespace = parser.parse_args(args)
            return True, ns.config
        except argparse.ArgumentError as e:
            message = StringIO()
            parser.print_help(message)
            message.write(str(e))
            return False, message.getvalue()

    def build(self) -> Context:
        clock = ClockImpl()
        loop = asyncio.get_event_loop()
        client = KubeClientImpl(self.settings.k8s, loop)

        executor_context = ExecutorContext(
            application_controller_client=Client(base_url=self.settings.placement.application_controller_endpoint),
            zone_api_factory=ZoneApiFactoryImpl(self.settings.placement),
            kube_client=client,
        )

        context = Context(clock, executor_context, client, self.settings, loop)
        return context
