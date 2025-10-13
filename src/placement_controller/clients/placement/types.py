from typing import Union

from placement_controller.api.model import BidRequestModel, BidResponseModel, ErrorResponse


class PlacementClient:

    async def bid(
        self,
        bid: BidRequestModel,
    ) -> Union[BidResponseModel, ErrorResponse]:
        raise NotImplementedError
