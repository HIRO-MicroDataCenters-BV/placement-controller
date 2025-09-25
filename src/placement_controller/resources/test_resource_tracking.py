import asyncio
from unittest import TestCase

from placement_controller.clients.k8s.fake_client import FakeClient


class ResourceTrackingImplTest(TestCase):
    runner: asyncio.Runner
    client: FakeClient

    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.client = FakeClient()

    def test_list_nodes(self):
        self.fail("not implemented")
