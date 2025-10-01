from typing import Callable, Dict, List, Optional

from dataclasses import dataclass, field
from decimal import Decimal

from placement_controller.api.model import BidCriteria
from placement_controller.resources.node import Node
from placement_controller.resources.pod import Pod
from placement_controller.resources.trace_log import TraceLog


@dataclass
class NodeInfo:
    name: str
    allocatable: Dict[str, Decimal] = field(default_factory=dict)
    requests: Dict[str, Decimal] = field(default_factory=dict)
    limits: Dict[str, Decimal] = field(default_factory=dict)
    free_resources: Optional[Dict[str, Decimal]] = None

    @staticmethod
    def from_node(node: Node) -> "NodeInfo":
        return NodeInfo(name=node.get_name(), allocatable=node.get_allocatable())

    def add(self, pod: Pod) -> None:
        self.free_resources = None
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

    def add_pod_requests_limits(self, requests: Dict[str, Decimal], limits: Dict[str, Decimal]) -> None:
        self.free_resources = None
        for resource_name, quantity in requests.items():
            total = self.requests.get(resource_name, Decimal(0))
            total += quantity
            self.requests[resource_name] = total

        for resource_name, quantity in limits.items():
            total = self.limits.get(resource_name, Decimal(0))
            total += quantity
            self.limits[resource_name] = total

    def get_free_resources(self) -> Dict[str, Decimal]:
        if self.free_resources is None:
            self.free_resources = dict()
            for resource, allocatable in self.allocatable.items():
                used = self.requests.get(resource, self.limits.get(resource, Decimal(0)))
                free = allocatable - used
                self.free_resources[resource] = free
        return self.free_resources

    def try_place(
        self,
        requests: Dict[str, Decimal],
        limits: Dict[str, Decimal],
        criteria: List[BidCriteria],
        log: TraceLog,
    ) -> bool:
        free_resources = self.get_free_resources()
        for criterio in criteria:
            free = free_resources.get(str(criterio), Decimal(0))
            consume = requests.get(criterio, limits.get(criterio, Decimal(0)))
            if free - consume < 0:
                log.log(f"Node {self.name} placement rejected. Not enough {criterio}.")
                return False
        return True


def node_info_comparator(criteria: List[BidCriteria]) -> Callable[[NodeInfo, NodeInfo], int]:
    def cmp_func(n1: NodeInfo, n2: NodeInfo) -> int:
        n1_free = n1.get_free_resources()
        n2_free = n2.get_free_resources()
        for criterio in criteria:
            n1_value = n1_free.get(criterio)
            n2_value = n2_free.get(criterio)
            if n1_value is None and n2_value is None:
                continue
            elif n1_value is None:
                return 1
            elif n2_value is None:
                return 1
            else:
                if n1_value == n2_value:
                    continue
                else:
                    return -1 if n1_value < n2_value else 1
        return 0

    return cmp_func
