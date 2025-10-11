from typing import Mapping, Set, Union

import asyncio
from decimal import Decimal

from placement_client import models
from placement_client.api.default import application_bid
from placement_client.client import Client

from placement_controller.api.model import (
    BidRequestModel,
    BidResponseModel,
    BidStatus,
    ErrorResponse,
    Metric,
    MetricUnit,
    MetricValue,
)
from placement_controller.clients.k8s.client import NamespacedName
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
        zone_to_client = [
            (zone, context.zone_api_factory.create(zone))
            for zone in self.zones
            if not context.zone_api_factory.is_local(zone)
        ]
        queries = [self.query_one(client) for (_, client) in zone_to_client]

        responses = await asyncio.gather(*queries)

        zone_to_response = {zone: response for ((zone, _), response) in zip(zone_to_client, responses)}

        return BidActionResult(zone_to_response, self.name, self.action_id)

    async def query_one(self, client: Client) -> BidResponseOrError:
        api_response = await application_bid.asyncio(
            client=client, body=BidAction.to_request(self.request, self.action_id)
        )
        response: BidResponseOrError
        if not api_response:
            response = ErrorResponse(status=500, code="INTERNAL_ERROR", msg="Received empty response")
        elif isinstance(api_response, models.BidResponseModel):
            response = BidAction.to_response(api_response)
        elif isinstance(api_response, models.ErrorResponse):
            response = ErrorResponse(status=api_response.status, code=api_response.code, msg=api_response.msg or None)
        elif isinstance(api_response, models.HTTPValidationError):
            response = ErrorResponse(status=422, code="VALIDATION_ERROR", msg=str(api_response))

        return response

    @staticmethod
    def to_request(request: BidRequestModel, action_id: ActionId) -> models.BidRequestModel:
        return models.BidRequestModel(
            id=action_id,
            spec=request.spec,
            bid_criteria=[models.BidCriteria(criteria) for criteria in request.bid_criteria],
            metrics=[models.Metric(metric) for metric in request.metrics],
        )

    @staticmethod
    def to_response(bid_response: models.BidResponseModel) -> BidResponseModel:
        def to_metric_value(m: models.MetricValue) -> MetricValue:
            return MetricValue(id=Metric(m.id), value=Decimal(m.value), unit=MetricUnit(m.unit))

        return BidResponseModel(
            id=bid_response.id,
            status=BidStatus(bid_response.status),
            reason=bid_response.reason or None,
            msg=bid_response.msg or None,
            metrics=[to_metric_value(m) for m in bid_response.metrics],
        )
