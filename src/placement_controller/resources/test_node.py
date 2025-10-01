from decimal import Decimal
from unittest import TestCase

from placement_controller.resource_fixture import ResourceTestFixture
from placement_controller.resources.node import Node
from placement_controller.resources.node_info import NodeInfo
from placement_controller.resources.pod import Pod


class NodeInfoTest(TestCase, ResourceTestFixture):

    def test_empty_node(self):
        node = Node(self.simple_node())
        node_info = NodeInfo.from_node(node)

        self.assertEqual(
            {"cpu": Decimal("10"), "ephemeral-storage": Decimal("134950129664"), "memory": Decimal("8218034176")},
            node_info.get_free_resources(),
        )

    def test_pod(self):
        node = Node(self.simple_node())
        pod = Pod(self.simple_pod())

        node_info = NodeInfo.from_node(node)
        node_info.add(pod)

        self.assertEqual(
            {"cpu": Decimal("9.900"), "ephemeral-storage": Decimal("134950129664"), "memory": Decimal("8113176576")},
            node_info.get_free_resources(),
        )


# TODO sort nodes
