from typing import Mapping, Set, Union

import asyncio

from loguru import logger

from placement_controller.api.model import (
    BidRequestModel,
    BidResponseModel,
    ErrorResponse,
)
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.clients.placement.types import PlacementClient
from placement_controller.core.scheduling_state import FSMOperation, ScaleDirection
from placement_controller.jobs.types import Action, ActionId, ActionResult, ExecutorContext

BidResponseOrError = Union[BidResponseModel, ErrorResponse]
ZoneId = str


class BidActionResult(ActionResult):
    response: Mapping[ZoneId, BidResponseOrError]

    def __init__(self, response: Mapping[ZoneId, BidResponseOrError], name: NamespacedName, action_id: ActionId):
        super().__init__(name, action_id)
        self.response = response

    def is_success(self) -> bool:
        return any([not isinstance(ok_or_error, ErrorResponse) for ok_or_error in self.response.values()])


class BidAction(Action[BidActionResult]):
    operation: FSMOperation
    request: BidRequestModel

    def __init__(
        self,
        operation: FSMOperation,
        request: BidRequestModel,
        name: NamespacedName,
    ):
        super().__init__(name, request.id)
        self.request = request
        self.operation = operation

    async def run(self, context: ExecutorContext) -> BidActionResult:

        bid_zones = self.determine_bid_zones()

        logger.info(f"{self.name.to_string()}: sending bid request to zones: {bid_zones}")

        zone_to_client = [(zone, context.zone_api_factory.create(zone)) for zone in bid_zones]
        queries = [self.query_one(client) for (_, client) in zone_to_client]
        responses = await asyncio.gather(*queries)

        zone_to_response = {zone: response for ((zone, _), response) in zip(zone_to_client, responses)}

        logger.info(f"{self.name.to_string()}: received responses {len(zone_to_response)}")

        return BidActionResult(zone_to_response, self.name, self.action_id)

    def determine_bid_zones(self) -> Set[str]:
        if self.operation.direction == ScaleDirection.UPSCALE:
            return self.operation.available_zones - self.operation.current_zones
        elif self.operation.direction == ScaleDirection.DOWNSCALE:
            return self.operation.current_zones
        logger.error(f"determine_bid_zones: unexpected direction {self.operation.direction}")
        return set()

    async def query_one(self, client: PlacementClient) -> BidResponseOrError:
        try:
            return await client.bid(self.request)
        except Exception as e:
            return ErrorResponse(status=500, code="INTERNAL_ERROR", msg=str(e))
