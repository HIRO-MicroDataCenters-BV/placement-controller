from unittest import TestCase

from application_client.models.application_spec import ApplicationSpec
from application_client.models.pod_resources import PodResources
from application_client.models.pod_resources_limits import PodResourcesLimits
from application_client.models.pod_resources_requests import PodResourcesRequests
from application_client.models.resource_id import ResourceId

from placement_controller.api.model import BidCriteria
from placement_controller.resource_fixture import ResourceTestFixture
from placement_controller.resources.node import Node
from placement_controller.resources.placement import GreedyPlacement
from placement_controller.resources.types import NodeInfo


class PlacementTest(TestCase, ResourceTestFixture):
    placement: GreedyPlacement
    node1: NodeInfo
    node2: NodeInfo
    node3: NodeInfo

    pod1: PodResources
    pod2: PodResources
    pod3: PodResources

    def setUp(self) -> None:
        self.node1 = NodeInfo.from_node(Node(self.make_node("node1", 2, 32 * self.GIGA, 512 * self.GIGA, 0)))
        self.node2 = NodeInfo.from_node(Node(self.make_node("node2", 4, 16 * self.GIGA, 512 * self.GIGA, 1)))
        self.node3 = NodeInfo.from_node(Node(self.make_node("node3", 6, 8 * self.GIGA, 512 * self.GIGA, 0)))

        self.pod1 = PodResources(
            id=ResourceId(name="pod1", namespace="test"),
            replica=1,
            requests=PodResourcesRequests.from_dict({"cpu": 1, "memory": 6 * self.GIGA}),
            limits=PodResourcesLimits.from_dict({"cpu": 2}),
        )
        self.pod2 = PodResources(
            id=ResourceId(name="pod2", namespace="test"),
            replica=1,
            requests=PodResourcesRequests.from_dict({"cpu": 3}),
            limits=PodResourcesLimits.from_dict({"cpu": 4}),
        )
        self.pod3 = PodResources(
            id=ResourceId(name="pod3", namespace="test"),
            replica=1,
            requests=PodResourcesRequests.from_dict({"cpu": 1}),
            limits=PodResourcesLimits.from_dict({"cpu": 2}),
        )

    def test_placement_empty(self):
        self.placement = GreedyPlacement(
            nodes=[],
            spec=ApplicationSpec(id=ResourceId(name="test", namespace="test"), resources=[]),
            bid_criteria=[],
        )

        result = self.placement.try_place()

        self.assertTrue(result.is_success)
        self.assertEqual(result.trace.get_raw(), ["-- result --"])

    def test_placement_pod(self):
        self.placement = GreedyPlacement(
            nodes=[self.node1, self.node2, self.node3],
            spec=ApplicationSpec(id=ResourceId(name="test", namespace="test"), resources=[self.pod1]),
            bid_criteria=[BidCriteria.cpu, BidCriteria.memory],
        )

        result = self.placement.try_place()

        self.assertTrue(result.is_success)
        self.assertEqual(
            result.trace.get_raw(),
            [
                "Instance 0 of pod test/pod1 is assigned to node node1.",
                "-- result --",
                " - pod test/pod1 is bound to nodes: node1",
            ],
        )

    def test_placement_pod_failure(self):
        self.placement = GreedyPlacement(
            nodes=[self.node1],
            spec=ApplicationSpec(id=ResourceId(name="test", namespace="test"), resources=[self.pod2]),
            bid_criteria=[BidCriteria.cpu, BidCriteria.memory],
        )

        result = self.placement.try_place()

        self.assertFalse(result.is_success())
        self.assertEqual(
            result.trace.get_raw(),
            [
                "Node node1 placement rejected. Not enough cpu.",
                "Failed to bind replica #0 of pod test/pod2.",
                "-- result --",
                " - unbounded pods test/pod2",
            ],
        )
