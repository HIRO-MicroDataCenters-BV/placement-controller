from typing import Dict, List, Union

from loguru import logger

from placement_controller.api.model import BidResponseModel, ErrorResponse
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.application import AnyApplication
from placement_controller.jobs.bid_action import BidResponseOrError, ZoneId
from placement_controller.jobs.types import Action, ActionId, ActionResult, ExecutorContext
from placement_controller.membership.types import PlacementZone


class DecisionActionResult(ActionResult):
    result: Union[List[PlacementZone], ErrorResponse]

    def __init__(self, result: Union[List[PlacementZone], ErrorResponse], name: NamespacedName, action_id: ActionId):
        super().__init__(name, action_id)
        self.result = result

    def is_success(self) -> bool:
        return not isinstance(self.result, ErrorResponse)


class DecisionAction(Action[DecisionActionResult]):
    bids: Dict[ZoneId, BidResponseOrError]
    application: AnyApplication

    def __init__(
        self,
        bids: Dict[ZoneId, BidResponseOrError],
        application: AnyApplication,
        name: NamespacedName,
        action_id: ActionId,
    ):
        super().__init__(name, action_id)
        self.bids = bids
        self.application = application

    async def run(self, _: ExecutorContext) -> DecisionActionResult:
        result: Union[List[PlacementZone], ErrorResponse]
        valid_responses = [(zone, bid) for zone, bid in self.bids.items() if isinstance(bid, BidResponseModel)]
        if len(valid_responses) == 0:
            logger.error(f"No valid bid responses for application {self.name}")
            result = ErrorResponse(status=500, code="APPLICATION_ERROR", msg="No valid bid responses for application.")
        else:

            result = []

        return DecisionActionResult(result, self.name, self.action_id)
