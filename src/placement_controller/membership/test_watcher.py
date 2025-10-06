import asyncio

from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.k8s.client import GroupVersionKind, NamespacedName
from placement_controller.clients.k8s.fake_client import FakeClient
from placement_controller.membership.types import MeshPeer
from placement_controller.membership.watcher import MembershipWatcher
from placement_controller.resource_fixture import ResourceTestFixture


class MembershipWatcherTest(AsyncTestFixture, ResourceTestFixture):
    client: FakeClient
    watcher: MembershipWatcher
    task: asyncio.Task[None]
    gvk: GroupVersionKind

    def setUp(self) -> None:
        super().setUp()
        self.gvk = MeshPeer.GVK
        self.client = FakeClient()
        self.watcher = MembershipWatcher(self.client, self.terminated)
        self.task = self.loop.create_task(self.watcher.start())

    def tearDown(self) -> None:
        self.task.cancel()
        super().tearDown()

    def test_create(self):
        object = self.simple_pod()
        self.loop.run_until_complete(self.client.patch(self.gvk, object))

        self.wait_for_condition(2, lambda: len(self.watcher.get_objects()) == 1)

    def test_update(self):
        object = self.simple_pod()
        self.loop.run_until_complete(self.client.patch(self.gvk, object))

        self.wait_for_condition(2, lambda: len(self.watcher.get_objects()) == 1)

        object["spec"]["scheduler"] = "set"
        self.loop.run_until_complete(self.client.patch(self.gvk, object))

        def test_property() -> bool:
            obj: MeshPeer = self.watcher.get_objects()[0]
            return obj.object["spec"].get("scheduler") == "set"  # type: ignore

        self.wait_for_condition(2, test_property)

    def test_delete(self):
        object = self.simple_pod()

        self.loop.run_until_complete(self.client.patch(self.gvk, object))
        self.wait_for_condition(2, lambda: len(self.watcher.get_objects()) == 1)

        self.loop.run_until_complete(self.client.delete(self.gvk, NamespacedName(name="nginx", namespace="test")))
        self.wait_for_condition(2, lambda: len(self.watcher.get_objects()) == 0)
