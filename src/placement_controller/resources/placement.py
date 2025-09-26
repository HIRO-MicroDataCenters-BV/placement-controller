from typing import List

from application_client.models.application_spec import ApplicationSpec

from placement_controller.api.model import BidCriteria, Metric
from placement_controller.resources.types import NodeInfo


class PlacementResult:
    pass


class GreedyPlacement:
    nodes: List[NodeInfo]
    spec: ApplicationSpec
    bid_criteria: List[BidCriteria]
    metrics: List[Metric]

    def __init__(
        self, nodes: List[NodeInfo], spec: ApplicationSpec, bid_criteria: List[BidCriteria], metrics: List[Metric]
    ):
        self.nodes = nodes
        self.spec = spec
        self.bid_criteria = bid_criteria
        self.metrics = metrics

    def try_bind(self) -> PlacementResult:
        return PlacementResult()
