import asyncio
from unittest import TestCase

from placement_controller.clients.k8s.fake_client import FakeClient
from placement_controller.resources.resource_tracking import ResourceTrackingImpl
from placement_controller.resources.types import ResourceTracking


class ResourceTrackingImplTest(TestCase):
    client: FakeClient
    tracking: ResourceTracking
    terminated: asyncio.Event
    loop: asyncio.AbstractEventLoop

    def setUp(self) -> None:
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.terminated = asyncio.Event()
        self.client = FakeClient()

        self.tracking = ResourceTrackingImpl(self.client, self.terminated)

    def tearDown(self) -> None:
        self.terminated.set()
        self.loop.close()

    def test_list_nodes(self):
        self.fail("not implemented")
