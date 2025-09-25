from placement_controller.api.model import BidRequestModel, BidResponseModel, BidStatus
from placement_controller.clients.k8s.client import KubeClient


class ResourceManagement:
    client: KubeClient

    def __init__(self, client: KubeClient):
        self.client = client

    def application_bid(self, bid: BidRequestModel) -> BidResponseModel:

        return BidResponseModel(id=bid.id, status=BidStatus.rejected, reason=None, msg=None, metrics=[])
