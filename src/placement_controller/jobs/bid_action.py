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
    zones: Set[str]
    request: BidRequestModel

    def __init__(self, zones: Set[str], request: BidRequestModel, name: NamespacedName):
        super().__init__(name, request.id)
        self.request = request
        self.zones = zones

    async def run(self, context: ExecutorContext) -> BidActionResult:

        logger.info(f"{self.name.to_string()}: sending bid request to zones: {self.zones}")

        zone_to_client = [(zone, context.zone_api_factory.create(zone)) for zone in self.zones]
        queries = [self.query_one(client) for (_, client) in zone_to_client]

        responses = await asyncio.gather(*queries)

        zone_to_response = {zone: response for ((zone, _), response) in zip(zone_to_client, responses)}

        logger.info(f"{self.name.to_string()}: received responses {len(zone_to_response)}")

        return BidActionResult(zone_to_response, self.name, self.action_id)

    async def query_one(self, client: PlacementClient) -> BidResponseOrError:
        return await client.bid(self.request)
