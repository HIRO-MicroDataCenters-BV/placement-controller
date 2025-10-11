from placement_controller.api.model import BidRequestModel, BidResponseModel
from placement_controller.resources.types import ResourceManagement


class FakeResourceManagement(ResourceManagement):
    response: BidResponseModel

    def application_bid(self, bid: BidRequestModel) -> BidResponseModel:
        return self.response

    def mock_response(self, response: BidResponseModel) -> None:
        self.response = response
