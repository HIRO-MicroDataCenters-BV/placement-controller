from placement_controller.api.model import BidRequestModel, BidResponseModel, BidStatus
from placement_controller.clients.k8s.client import KubeClient
from placement_controller.resources.types import ResourceTracking


class ResourceManagement:
    client: KubeClient
    resource_tracking: ResourceTracking

    def __init__(self, client: KubeClient, resource_tracking: ResourceTracking):
        self.client = client
        self.resource_tracking = resource_tracking

    def application_bid(self, bid: BidRequestModel) -> BidResponseModel:

        # nodes = self.resource_tracking.list_nodes()

        return BidResponseModel(id=bid.id, status=BidStatus.rejected, reason=None, msg=None, metrics=[])
