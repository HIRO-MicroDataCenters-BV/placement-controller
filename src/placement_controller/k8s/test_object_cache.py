import asyncio
from unittest import TestCase

from placement_controller.clients.k8s.fake_client import FakeClient


class ObjectCacheTest(TestCase):
    runner: asyncio.Runner
    client: FakeClient

    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.client = FakeClient()

    def test_create(self):
        self.fail("not implemented")

    def test_update(self):
        self.fail("not implemented")

    def test_delete(self):
        self.fail("not implemented")
