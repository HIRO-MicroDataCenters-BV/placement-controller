from typing import Any, Dict

import asyncio
from unittest import TestCase

from app.clients.k8s.client import GroupVersionKind, NamespacedName
from app.clients.k8s.event import EventType, KubeEvent
from app.clients.k8s.fake_client import FakeClient


class FakeClientTest(TestCase):
    runner: asyncio.Runner
    client: FakeClient
    gvk: GroupVersionKind
    name: NamespacedName

    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.client = FakeClient()
        self.gvk = GroupVersionKind(group="dcp.hiro.io", version="v1", kind="AnyApplication")
        self.name = NamespacedName(name="nginx-app", namespace="test")

    def test_get(self):
        object = self.loop.run_until_complete(self.client.get(self.gvk, self.name))
        self.assertEqual(object, None)

    def test_patch(self):
        object = self.loop.run_until_complete(self.client.get(self.gvk, self.name))
        self.assertEqual(object, None)

        object = self.make_object()
        actual = self.loop.run_until_complete(self.client.patch(self.gvk, object))
        object["metadata"]["resourceVersion"] = "1"
        object["metadata"]["uid"] = "1"
        self.assertEqual(object, actual)

        actual = self.loop.run_until_complete(self.client.get(self.gvk, self.name))
        self.assertEqual(object, actual)

    def test_patch_status(self):
        object = self.make_object()

        self.loop.run_until_complete(self.client.patch(self.gvk, object))

        status = self.make_status()
        actual = self.loop.run_until_complete(self.client.patch_status(self.gvk, self.name, status))

        object["status"] = status["status"]
        object["metadata"]["resourceVersion"] = "2"
        object["metadata"]["uid"] = "1"

        self.assertEqual(object, actual)

    def test_lifecycle(self):
        sub_id, queue = self.client.watch(self.gvk, "test", "0", 0)

        # create
        object = self.make_object()
        self.loop.run_until_complete(self.client.patch(self.gvk, object))
        object["metadata"]["resourceVersion"] = "1"
        object["metadata"]["uid"] = "1"

        actual_event = self.loop.run_until_complete(queue.get())
        expected_event = KubeEvent(event=EventType.ADDED, version=1, object=object)
        self.assertEqual(actual_event, expected_event)

        # update
        status = self.make_status()
        self.loop.run_until_complete(self.client.patch_status(self.gvk, self.name, status))
        object["status"] = status["status"]
        object["metadata"]["resourceVersion"] = "2"

        actual_event = self.loop.run_until_complete(queue.get())
        expected_event = KubeEvent(event=EventType.MODIFIED, version=2, object=object)
        self.assertEqual(actual_event, expected_event)

        # delete
        self.loop.run_until_complete(self.client.delete(self.gvk, self.name))
        object["metadata"]["resourceVersion"] = "3"

        actual_event = self.loop.run_until_complete(queue.get())
        expected_event = KubeEvent(event=EventType.DELETED, version=3, object=object)
        self.assertEqual(actual_event, expected_event)

        self.client.stop_watch(sub_id)

    def make_object(self) -> Dict[str, Any]:
        return {
            "apiVersion": "dcp.hiro.io/v1",
            "kind": "AnyApplication",
            "metadata": {
                "name": "nginx-app",
                "namespace": "test",
            },
            "spec": {
                "application": {
                    "helm": {
                        "chart": "nginx-ingress",
                        "namespace": "nginx",
                        "repository": "https://helm.nginx.com/stable",
                        "version": "2.0.1",
                    }
                },
                "placement-strategy": {"strategy": "Local"},
                "recover-strategy": {"max-retries": 3, "tolerance": 1},
                "zones": 1,
            },
        }

    def make_status(self) -> Dict[str, Any]:
        return {
            "status": {
                "state": "old",
                "owner": "zone1",
                "placements": [
                    {
                        "node-affinity": None,
                        "zone": "zone1",
                    }
                ],
                "conditions": [
                    {
                        "lastTransitionTime": "2025-06-04T09:40:41Z",
                        "status": "status",
                        "type": "conditionType",
                        "zoneId": "zone1",
                        "zoneVersion": "1",
                    }
                ],
            }
        }
