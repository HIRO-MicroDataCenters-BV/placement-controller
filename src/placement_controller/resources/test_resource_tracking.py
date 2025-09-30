import asyncio
from decimal import Decimal

from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.k8s.fake_client import FakeClient
from placement_controller.resource_fixture import ResourceTestFixture
from placement_controller.resources.resource_tracking import ResourceTrackingImpl
from placement_controller.resources.types import NodeInfo, ResourceTracking


class ResourceTrackingImplTest(AsyncTestFixture, ResourceTestFixture):
    client: FakeClient
    tracking: ResourceTracking
    terminated: asyncio.Event
    loop: asyncio.AbstractEventLoop

    def setUp(self) -> None:
        super().setUp()
        self.client = FakeClient()

        self.tracking = ResourceTrackingImpl(self.client, self.terminated)
        self.task = self.loop.create_task(self.tracking.start())
        self.wait_for_condition(2, lambda: self.tracking.is_subscription_active())

    def tearDown(self) -> None:
        self.task.cancel()
        super().tearDown()

    def test_list_nodes_empty(self):
        node = self.simple_node()

        self.loop.run_until_complete(self.client.patch(self.node_gvk, node))
        self.wait_for_condition(2, lambda: len(self.tracking.list_nodes()) == 1)

        node_infos = self.tracking.list_nodes()
        self.assertEqual(
            node_infos,
            [
                NodeInfo(
                    name="node1",
                    allocatable={
                        "cpu": Decimal("10"),
                        "ephemeral-storage": Decimal("134950129664"),
                        "memory": Decimal("8218034176"),
                    },
                )
            ],
        )

    def test_list_nodes_with_pod(self):
        node = self.simple_node()
        pod = self.simple_pod()

        node_name = node["metadata"]["name"]
        pod["spec"]["nodeName"] = node_name

        self.loop.run_until_complete(self.client.patch(self.node_gvk, node))
        self.loop.run_until_complete(self.client.patch(self.pod_gvk, pod))

        self.wait_for_condition(2, lambda: len(self.tracking.list_nodes()) == 1)
        node_infos = self.tracking.list_nodes()
        free_resources = node_infos[0].get_free_resources()
        self.assertEqual(
            free_resources,
            {"cpu": Decimal("9.900"), "ephemeral-storage": Decimal("134950129664"), "memory": Decimal("8113176576")},
        )
