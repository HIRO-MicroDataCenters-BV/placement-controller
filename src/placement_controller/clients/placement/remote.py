from typing import Union

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
from placement_controller.clients.placement.types import PlacementClient


class RemotePlacementClient(PlacementClient):
    client: Client

    def __init__(self, client: Client):
        self.client = client

    async def bid(
        self,
        bid: BidRequestModel,
    ) -> Union[BidResponseModel, ErrorResponse]:
        api_response = await application_bid.asyncio(
            client=self.client, body=RemotePlacementClient.to_client_request(bid)
        )
        response: Union[BidResponseModel, ErrorResponse]
        if not api_response:
            response = ErrorResponse(status=500, code="INTERNAL_ERROR", msg="Received empty response")
        elif isinstance(api_response, models.BidResponseModel):
            response = RemotePlacementClient.from_client_response(api_response)
        elif isinstance(api_response, models.ErrorResponse):
            response = ErrorResponse(status=api_response.status, code=api_response.code, msg=api_response.msg or None)
        elif isinstance(api_response, models.HTTPValidationError):
            response = ErrorResponse(status=422, code="VALIDATION_ERROR", msg=str(api_response))
        return response

    @staticmethod
    def to_client_request(bid: BidRequestModel) -> models.BidRequestModel:
        return models.BidRequestModel(
            id=bid.id,
            spec=bid.spec,
            bid_criteria=[models.BidCriteria(criteria) for criteria in bid.bid_criteria],
            metrics=[models.Metric(metric) for metric in bid.metrics],
        )

    @staticmethod
    def from_client_response(bid_response: models.BidResponseModel) -> BidResponseModel:
        def to_metric_value(m: models.MetricValue) -> MetricValue:
            return MetricValue(id=Metric(m.id), value=Decimal(m.value), unit=MetricUnit(m.unit))

        return BidResponseModel(
            id=bid_response.id,
            status=BidStatus(bid_response.status),
            reason=bid_response.reason or None,
            msg=bid_response.msg or None,
            metrics=[to_metric_value(m) for m in bid_response.metrics],
        )
