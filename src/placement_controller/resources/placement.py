from typing import Dict, List, Optional, Set

import functools
from dataclasses import dataclass, field
from decimal import Decimal

from application_client.models.application_spec import ApplicationSpec
from application_client.models.pod_resources import PodResources
from application_client.models.resource_id import ResourceId
from kubernetes.utils.quantity import parse_quantity

from placement_controller.api.model import BidCriteria
from placement_controller.resources.trace_log import TraceLog
from placement_controller.resources.types import NodeInfo, node_info_comparator

PodName = str
NodeName = str


@dataclass
class PodBinding:
    id: ResourceId
    replica: int


@dataclass
class PlacementResult:
    bound_pods: Dict[PodBinding, NodeName] = field(default_factory=dict)
    unbound_pods: Set[PodName] = field(default_factory=set)
    reason: Optional[str] = None
    trace: TraceLog = field(default_factory=TraceLog)

    def bind_pod(self, pod: PodBinding, node: NodeName) -> None:
        self.bound_pods[pod] = node

    def unbind_pod(self, pod: PodName) -> None:
        self.unbound_pods.add(pod)

    def is_success(self) -> bool:
        return len(self.unbound_pods) == 0


class GreedyPlacement:
    nodes: List[NodeInfo]
    spec: ApplicationSpec
    bid_criteria: List[BidCriteria]

    def __init__(self, nodes: List[NodeInfo], spec: ApplicationSpec, bid_criteria: List[BidCriteria]):
        self.nodes = sorted(nodes, key=functools.cmp_to_key(node_info_comparator(bid_criteria)))
        self.spec = spec
        self.bid_criteria = bid_criteria

    def try_place(self) -> PlacementResult:
        placement_result = PlacementResult()
        trace = placement_result.trace
        for resource in self.spec.resources:
            if isinstance(resource, PodResources):
                instance = 0
                requests = {
                    resource_name: parse_quantity(resource.requests[resource_name])
                    for resource_name in resource.requests.additional_keys
                }
                limits = {
                    resource_name: parse_quantity(resource.limits[resource_name])
                    for resource_name in resource.limits.additional_keys
                }
                while instance < resource.replica:
                    node_info = self.find_node(requests, limits, trace)
                    if node_info is not None:
                        node_info.add_pod_requests_limits(requests, limits)
                        placement_result.bind_pod(PodBinding(resource.id, instance), node_info.name)
                        trace.log(f"Instance {instance} of pod {resource.id} is assigned to node {node_info.name}.")
                    else:
                        placement_result.unbind_pod(str(resource.id))
                        trace.log(f"Failed to bind {instance} of pod {resource.id}.")
                    instance += 1

        return placement_result

    def find_node(
        self, requests: Dict[str, Decimal], limits: Dict[str, Decimal], trace: TraceLog
    ) -> Optional[NodeInfo]:
        for node_info in self.nodes:
            can_place = node_info.try_place(requests, limits, self.bid_criteria, trace)
            if can_place:
                return node_info
        return None
