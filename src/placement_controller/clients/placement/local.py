from typing import Union

from placement_controller.api.model import BidRequestModel, BidResponseModel, ErrorResponse
from placement_controller.clients.placement.types import PlacementClient
from placement_controller.resources.resource_managment import ResourceManagement


class LocalPlacementClient(PlacementClient):
    resource_management: ResourceManagement

    def __init__(self, resource_management: ResourceManagement):
        self.resource_management = resource_management

    async def bid(self, bid: BidRequestModel) -> Union[BidResponseModel, ErrorResponse]:
        return self.resource_management.application_bid(bid)
