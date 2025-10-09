from typing import Callable, Dict, List, Tuple, Union

import functools

from loguru import logger

from placement_controller.api.model import BidResponseModel, ErrorResponse, Metric
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
            criteria_priority = [Metric.cost, Metric.energy]
            sorted_responses = sorted(
                valid_responses,
                key=functools.cmp_to_key(bid_response_comparator(criteria_priority)),
            )
            replica = self.get_replica_count()
            first_responses = sorted_responses[:replica]

            result = [PlacementZone(id=response[0]) for response in first_responses]

        return DecisionActionResult(result, self.name, self.action_id)

    def get_replica_count(self) -> int:
        spec = self.application.get_spec()
        zones = spec.get("zones") or 1
        return int(zones)


def bid_response_comparator(
    criteria: List[Metric],
) -> Callable[[Tuple[str, BidResponseModel], Tuple[str, BidResponseModel]], int]:
    def cmp_func(r1: Tuple[str, BidResponseModel], r2: Tuple[str, BidResponseModel]) -> int:
        for criterio in criteria:
            _, resp1 = r1
            _, resp2 = r2
            m1 = resp1.get_metric_value(criterio)
            m2 = resp2.get_metric_value(criterio)

            m1_value = m1.value if m1 else None
            m2_value = m2.value if m2 else None

            if m1_value is None and m2_value is None:
                continue
            elif m1_value is None:
                return 1
            elif m2_value is None:
                return 1
            else:
                if m1_value == m2_value:
                    continue
                else:
                    return -1 if m1_value < m2_value else 1
        return 0

    return cmp_func
