from typing import List

from application_client.models.application_spec import ApplicationSpec

from placement_controller.api.model import BidRequestModel, BidResponseModel, Metric, MetricValue
from placement_controller.resources.node_info import NodeInfo


class ResourceTracking:

    async def start(self) -> None:
        raise NotImplementedError

    def list_nodes(self) -> List[NodeInfo]:
        raise NotImplementedError

    def is_subscription_active(self) -> bool:
        raise NotImplementedError


class ResourceManagement:

    def application_bid(self, bid: BidRequestModel) -> BidResponseModel:
        raise NotImplementedError


class ResourceMetrics:

    def estimate(self, spec: ApplicationSpec, metrics: List[Metric]) -> List[MetricValue]:
        raise NotImplementedError
