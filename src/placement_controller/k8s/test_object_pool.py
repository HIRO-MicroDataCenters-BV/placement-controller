from typing import Any, Callable, Dict

import asyncio
import datetime
from unittest import TestCase

from placement_controller.clients.k8s.client import GroupVersionKind, NamespacedName
from placement_controller.clients.k8s.fake_client import FakeClient
from placement_controller.clients.k8s.resource import BaseResource
from placement_controller.k8s.object_pool import ObjectPool


class TestResource(BaseResource):

    def __init__(self, object: Dict[str, Any]):
        super().__init__(object)


class ObjectPoolTest(TestCase):
    client: FakeClient
    pool: ObjectPool[TestResource]
    task: asyncio.Task[None]
    loop: asyncio.AbstractEventLoop
    gvk: GroupVersionKind

    def setUp(self) -> None:
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.gvk = GroupVersionKind("", "v1", "Pod")
        self.client = FakeClient()
        self.terminated = asyncio.Event()
        self.pool = ObjectPool[TestResource](TestResource, self.client, self.gvk, self.terminated)
        self.task = self.loop.create_task(self.pool.start())

    def tearDown(self) -> None:
        self.terminated.set()
        self.task.cancel()
        self.loop.close()

    def test_create(self):
        object = self.make_object()
        self.loop.run_until_complete(self.client.patch(self.gvk, object))

        self.wait_for_condition(2, lambda: len(self.pool.get_objects()) == 1)

    def test_update(self):
        object = self.make_object()
        self.loop.run_until_complete(self.client.patch(self.gvk, object))

        self.wait_for_condition(2, lambda: len(self.pool.get_objects()) == 1)

        object["spec"]["scheduler"] = "set"
        self.loop.run_until_complete(self.client.patch(self.gvk, object))

        def test_property() -> bool:
            obj: TestResource = self.pool.get_objects()[0]
            return obj.object["spec"].get("scheduler") == "set"  # type: ignore

        self.wait_for_condition(2, test_property)

    def test_delete(self):
        object = self.make_object()

        self.loop.run_until_complete(self.client.patch(self.gvk, object))
        self.wait_for_condition(2, lambda: len(self.pool.get_objects()) == 1)

        self.loop.run_until_complete(self.client.delete(self.gvk, NamespacedName(name="nginx", namespace="test")))
        self.wait_for_condition(2, lambda: len(self.pool.get_objects()) == 0)

    def wait_for_condition(self, seconds: int, conditionFunc: Callable[[], bool]) -> None:
        start = datetime.datetime.now()
        while start + datetime.timedelta(seconds=seconds) > datetime.datetime.now():
            if conditionFunc():
                return
            asyncio.run(asyncio.sleep(0.1))
        raise AssertionError("time is up.")

    def make_object(self) -> Dict[str, Any]:
        return {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": "nginx",
                "namespace": "test",
            },
            "spec": {"containers": [{"name": "nginx", "image": "nginx:1.14.2", "ports": [{"containerPort": 80}]}]},
        }
