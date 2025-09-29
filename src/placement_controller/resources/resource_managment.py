from typing import Any, Dict

import json

from application_client.models.application_spec import ApplicationSpec

from placement_controller.api.model import BidRequestModel, BidResponseModel, BidStatus
from placement_controller.clients.k8s.client import KubeClient
from placement_controller.resources.placement import GreedyPlacement
from placement_controller.resources.types import ResourceTracking


class ResourceManagement:
    client: KubeClient
    resource_tracking: ResourceTracking

    def __init__(self, client: KubeClient, resource_tracking: ResourceTracking):
        self.client = client
        self.resource_tracking = resource_tracking

    def application_bid(self, bid: BidRequestModel) -> BidResponseModel:
        nodes = self.resource_tracking.list_nodes()
        app_spec: Dict[str, Any] = json.loads(bid.spec)
        spec = ApplicationSpec.from_dict(app_spec)
        placement = GreedyPlacement(nodes, spec, bid.bid_criteria)

        result = placement.try_place()
        status = BidStatus.accepted if result.is_success() else BidStatus.rejected

        return BidResponseModel(id=bid.id, status=status, reason=result.reason, msg=result.trace.get_data(), metrics=[])
