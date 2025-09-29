from typing import Dict, List, Optional, Set

from dataclasses import dataclass, field

from application_client.models.application_spec import ApplicationSpec
from application_client.models.pod_resources import PodResources

from placement_controller.api.model import BidCriteria
from placement_controller.resources.types import NodeInfo

PodName = str
NodeName = str


@dataclass
class PlacementResult:
    bound_pods: Dict[PodName, NodeName] = field(default_factory=dict)
    unbound_pods: Set[PodName] = field(default_factory=set)
    reason: Optional[str] = None
    msg_log: Optional[str] = None

    def bind_pod(self, pod: PodName, node: NodeName, msg: str) -> None:
        self.bound_pods[pod] = node
        self.msg_log = (self.msg_log or "") + msg + "\n"

    def unbind_pod(self, pod: PodName, msg: str) -> None:
        self.unbound_pods.add(pod)
        self.msg_log = (self.msg_log or "") + msg + "\n"

    def is_success(self) -> bool:
        return len(self.unbound_pods) == 0


class GreedyPlacement:
    nodes: List[NodeInfo]
    spec: ApplicationSpec
    bid_criteria: Set[BidCriteria]

    def __init__(self, nodes: List[NodeInfo], spec: ApplicationSpec, bid_criteria: Set[BidCriteria]):
        self.nodes = nodes
        self.spec = spec
        self.bid_criteria = bid_criteria

    def try_place(self) -> PlacementResult:
        for resource in self.spec.resources:
            if isinstance(resource, PodResources):
                self.find_node(resource)
        return PlacementResult()

    def find_node(self, resource: PodResources) -> Optional[NodeInfo]:
        return None
