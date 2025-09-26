from typing import List

from dataclasses import dataclass

from placement_controller.resources.node import Node
from placement_controller.resources.pod import Pod


@dataclass
class NodeInfo:
    name: str

    @staticmethod
    def from_node(node: Node) -> "NodeInfo":
        node_info = NodeInfo(name=node.get_name())

        return node_info

    def add(self, pod: Pod) -> None:
        pass


class ResourceTracking:

    def start(self) -> None:
        raise NotImplementedError

    def list_nodes(self) -> List[NodeInfo]:
        raise NotImplementedError
