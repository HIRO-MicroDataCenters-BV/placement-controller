from typing import Callable, List, Mapping, Tuple, Union

import functools

from loguru import logger

from placement_controller.api.model import BidResponseModel, BidStatus, ErrorResponse, Metric
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.scheduling_state import FSMOperation, ScaleDirection
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
    bids: Mapping[ZoneId, BidResponseOrError]
    operation: FSMOperation
    criteria_priority: List[Metric]

    def __init__(
        self,
        bids: Mapping[ZoneId, BidResponseOrError],
        operation: FSMOperation,
        name: NamespacedName,
        action_id: ActionId,
    ):
        super().__init__(name, action_id)
        self.bids = bids
        self.operation = operation
        self.criteria_priority = [Metric.cost, Metric.energy]

    async def run(self, _: ExecutorContext) -> DecisionActionResult:
        result: Union[List[PlacementZone], ErrorResponse]
        valid_responses = [(zone, bid) for zone, bid in self.bids.items() if isinstance(bid, BidResponseModel)]
        accepted_responses = [(zone, bid) for zone, bid in valid_responses if bid.status == BidStatus.accepted]

        logger.info(
            f"{self.name.to_string()}: Making decision. Total responses: {len(self.bids)}, "
            + f"valid: {len(valid_responses)}, accepted {len(accepted_responses)}"
        )

        if self.operation.direction == ScaleDirection.UPSCALE:
            result = self.upscale_decision(accepted_responses)
        elif self.operation.direction == ScaleDirection.DOWNSCALE:
            result = self.downscale_decision(accepted_responses)
        else:
            result = ErrorResponse(
                status=500, code="APPLICATION_ERROR", msg=f"Invalid operation direction {self.operation.direction}."
            )
        return DecisionActionResult(result, self.name, self.action_id)

    def upscale_decision(
        self, responses: List[Tuple[ZoneId, BidResponseModel]]
    ) -> Union[List[PlacementZone], ErrorResponse]:
        result: Union[List[PlacementZone], ErrorResponse]
        if len(responses) == 0:
            logger.error(f"{self.name.to_string()}:  No valid and accepted bid responses for application.")
            result = ErrorResponse(status=500, code="APPLICATION_ERROR", msg="No valid bid responses for application.")
        else:
            responses_excluding_current_zones = [
                response for response in responses if response[0] not in self.operation.current_zones
            ]
            sorted_responses = sorted(
                responses_excluding_current_zones,
                key=functools.cmp_to_key(bid_response_comparator(self.criteria_priority)),
            )

            desired_replica = self.operation.required_replica
            current_zones = [PlacementZone(id=current_zone_id) for current_zone_id in self.operation.current_zones]
            upscale_replica = desired_replica - len(current_zones)

            chosen_responses = sorted_responses[:upscale_replica]

            upscale_zones = [PlacementZone(id=response[0]) for response in chosen_responses]
            result = current_zones + upscale_zones
            logger.info(f"{self.name.to_string()}: placements decided: {result}")
        return result

    def downscale_decision(
        self, responses: List[Tuple[ZoneId, BidResponseModel]]
    ) -> Union[List[PlacementZone], ErrorResponse]:
        desired_replica = self.operation.required_replica
        if desired_replica == 0:
            return []

        if len(responses) == 0:
            logger.error(
                f"{self.name.to_string()}:  No valid and accepted bid responses for application."
                + " Will pick any zones to downscale."
            )

        responses_including_current_zones = [
            response for response in responses if response[0] in self.operation.current_zones
        ]
        sorted_responses = sorted(
            responses_including_current_zones,
            key=functools.cmp_to_key(bid_response_comparator(self.criteria_priority)),
            reverse=True,
        )
        sorted_zones = [zone_id for zone_id, _ in sorted_responses]
        current_zones = self.operation.current_zones

        while len(current_zones) > desired_replica:
            if len(sorted_zones) > 0:
                head, sorted_zones = sorted_zones[0], sorted_zones[1:]
                current_zones.discard(head)
            else:
                current_zones.pop()
        result = [PlacementZone(id=zone_id) for zone_id in current_zones]
        return result


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
