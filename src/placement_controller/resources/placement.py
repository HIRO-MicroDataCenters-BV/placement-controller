from typing import List

from application_client.models.application_spec import ApplicationSpec

from placement_controller.resources.types import NodeInfo


class PlacementResult:
    pass


class GreedyPlacement:
    nodes: List[NodeInfo]

    def __init__(self, nodes: List[NodeInfo], spec: ApplicationSpec):
        self.nodes = nodes

    def try_bind(self) -> PlacementResult:
        return PlacementResult()
