import asyncio

from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.k8s.client import GroupVersionKind
from placement_controller.clients.k8s.fake_client import FakeClient
from placement_controller.resource_fixture import ResourceTestFixture
from placement_controller.resources.resource_tracking import ResourceTrackingImpl
from placement_controller.resources.types import ResourceTracking


class ResourceTrackingImplTest(AsyncTestFixture, ResourceTestFixture):
    client: FakeClient
    tracking: ResourceTracking
    terminated: asyncio.Event
    loop: asyncio.AbstractEventLoop
    node_gvk: GroupVersionKind
    pod_gvk: GroupVersionKind

    def setUp(self) -> None:
        super().setUp()
        self.client = FakeClient()
        self.pod_gvk = GroupVersionKind("", "v1", "Pod")
        self.node_gvk = GroupVersionKind("", "v1", "Node")
        self.tracking = ResourceTrackingImpl(self.client, self.terminated)

    def tearDown(self) -> None:
        super().tearDown()

    def test_list_nodes(self):
        node = self.simple_node()
        pod = self.simple_pod()

        node_name = node["metadata"]["name"]
        pod["spec"]["nodeName"] = node_name

        self.loop.run_until_complete(self.client.patch(self.node_gvk, node))
        self.loop.run_until_complete(self.client.patch(self.pod_gvk, pod))

        node_infos = self.tracking.list_nodes()

        self.assertEqual(node_infos, [])
