from typing import List, Optional, Tuple

import argparse
import asyncio
from argparse import Namespace
from io import StringIO

from app.clients.k8s.client_impl import KubeClientImpl
from app.context import Context
from app.pydantic_yaml import from_yaml
from app.settings import Settings
from app.util.clock_impl import ClockImpl


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
        k8s_client = KubeClientImpl(self.settings.k8s, asyncio.get_event_loop())

        context = Context(
            clock,
            k8s_client,
            self.settings,
        )
        return context
