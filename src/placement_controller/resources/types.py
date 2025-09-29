from typing import Dict, List

from dataclasses import dataclass, field
from decimal import Decimal

from placement_controller.resources.node import Node
from placement_controller.resources.pod import Pod


@dataclass
class NodeInfo:
    name: str
    allocatable: Dict[str, Decimal] = field(default_factory=dict)
    requests: Dict[str, Decimal] = field(default_factory=dict)
    limits: Dict[str, Decimal] = field(default_factory=dict)

    @staticmethod
    def from_node(node: Node) -> "NodeInfo":
        return NodeInfo(name=node.get_name(), allocatable=node.get_allocatable())

    def add(self, pod: Pod) -> None:
        NodeInfo.add_resources(self.requests, pod.get_requests())
        NodeInfo.add_resources(self.limits, pod.get_limits())

    @staticmethod
    def add_resources(totals: Dict[str, Decimal], resources_per_container: List[Dict[str, Dict[str, Decimal]]]) -> None:
        for container in resources_per_container:
            for _, container_resources in container.items():
                for resource_name, quantity in container_resources.items():
                    total = totals.get(resource_name, Decimal(0))
                    total += quantity
                    totals[resource_name] = total

    def get_free_resources(self) -> Dict[str, Decimal]:
        free_resources = dict()
        for resource, allocatable in self.allocatable.items():
            used = self.requests.get(resource, self.limits.get(resource, Decimal(0)))
            free = allocatable - used
            free_resources[resource] = free
        return free_resources


class ResourceTracking:

    def start(self) -> None:
        raise NotImplementedError

    def list_nodes(self) -> List[NodeInfo]:
        raise NotImplementedError
