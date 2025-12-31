from typing import Any, Dict

import json
from asyncio import Task
from decimal import Decimal

from application_client.models.application_spec import ApplicationSpec
from application_client.models.resource_id import ResourceId

from placement_controller.api.model import (
    BidCriteria,
    BidRequestModel,
    BidResponseModel,
    BidStatus,
    Metric,
    MetricValue,
    NamespacedNameModel,
    TraceLogRowModel,
)
from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.k8s.fake_client import FakeClient
from placement_controller.resource_fixture import ResourceTestFixture
from placement_controller.resources.resource_managment import ResourceManagementImpl
from placement_controller.resources.resource_metrics import MetricSettings, ResourceMetricsImpl
from placement_controller.resources.resource_tracking import ResourceTrackingImpl
from placement_controller.resources.types import ResourceManagement, ResourceTracking
from placement_controller.util.mock_clock import MockClock


class ResourceManagementTest(AsyncTestFixture, ResourceTestFixture):
    client: FakeClient
    clock: MockClock
    tracking: ResourceTracking
    resource_management: ResourceManagement
    task: Task[None]

    node1: Dict[str, Any]
    node2: Dict[str, Any]

    def setUp(self) -> None:
        super().setUp()
        self.clock = MockClock()
        self.client = FakeClient()
        self.tracking = ResourceTrackingImpl(self.client, self.terminated)
        self.task = self.loop.create_task(self.tracking.start())
        self.wait_for_condition(2, lambda: self.tracking.is_subscription_active())

        resource_metrics = ResourceMetricsImpl(config=MetricSettings(static_metrics=[]))

        self.resource_management = ResourceManagementImpl(
            "zone", self.clock, self.client, self.tracking, resource_metrics
        )

        self.node1 = self.make_node("node1", 2, 32 * self.GIGA, 512 * self.GIGA, 0)
        self.node2 = self.make_node("node2", 4, 16 * self.GIGA, 512 * self.GIGA, 1)

        self.loop.run_until_complete(self.client.patch(self.node_gvk, self.node1))
        self.loop.run_until_complete(self.client.patch(self.node_gvk, self.node2))

    def tearDown(self) -> None:
        self.task.cancel()
        super().tearDown()

    def test_application_bid(self):
        spec = ApplicationSpec(
            id=ResourceId(name="test", namespace="test"),
            resources=[self.make_pod_spec("pod1", 1, {"cpu": "2", "memory": "200Mi"}, {})],
        )
        spec_json = self.to_json_str(spec)
        bid = BidRequestModel(
            id="id",
            name=NamespacedNameModel(name="test", namespace="test"),
            spec=spec_json,
            bid_criteria=[BidCriteria.cpu, BidCriteria.memory],
            metrics={Metric.cost},
        )
        response = self.resource_management.application_bid(bid)

        self.assertEqual(
            response,
            BidResponseModel(
                id=bid.id,
                status=BidStatus.accepted,
                reason=None,
                trace=[
                    TraceLogRowModel(
                        timestamp=1000,
                        zone="zone",
                        name=NamespacedNameModel(name="test", namespace="test"),
                        msg="Instance 0 of pod test/pod1 is assigned to node node1.",
                    ),
                    TraceLogRowModel(
                        timestamp=1000,
                        zone="zone",
                        name=NamespacedNameModel(name="test", namespace="test"),
                        msg="-- placement result --",
                    ),
                    TraceLogRowModel(
                        timestamp=1000,
                        zone="zone",
                        name=NamespacedNameModel(name="test", namespace="test"),
                        msg=" - pod test/pod1 is bound to nodes: node1",
                    ),
                ],
                msg=None,
                metrics=[MetricValue(id=Metric.cost, value=Decimal(0.0), unit=Metric.cost.unit())],
            ),
        )

    def to_json_str(self, spec: ApplicationSpec) -> str:
        return json.dumps(spec.to_dict())
