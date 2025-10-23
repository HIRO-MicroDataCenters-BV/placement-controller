from typing import List, Optional, Union

from dataclasses import dataclass

from loguru import logger

from placement_controller.api.model import ErrorResponse
from placement_controller.clients.k8s.client import KubeClient, NamespacedName
from placement_controller.core.application import AnyApplication
from placement_controller.jobs.types import Action, ActionId, ActionResult, ExecutorContext
from placement_controller.membership.types import PlacementZone
from placement_controller.store.types import DecisionStore
from placement_controller.util.clock import Clock


@dataclass
class PlacementDecision:
    spec: str
    placements: List[PlacementZone]
    reason: str
    trace: str


class SetPlacementActionResult(ActionResult):
    result: Union[bool, ErrorResponse]

    def __init__(self, result: Union[bool, ErrorResponse], name: NamespacedName, action_id: ActionId):
        super().__init__(name, action_id)
        self.result = result

    def is_success(self) -> bool:
        return isinstance(self.result, ErrorResponse)


class SetPlacementAction(Action[SetPlacementActionResult]):
    decision: PlacementDecision

    def __init__(
        self,
        decision: PlacementDecision,
        name: NamespacedName,
        action_id: ActionId,
    ):
        super().__init__(name, action_id)
        self.decision = decision

    async def run(self, ctx: ExecutorContext) -> SetPlacementActionResult:
        logger.info(f"{self.name.to_string()}: setting placement zones {self.decision.placements}")

        result = await self.set_placement_zones(ctx.kube_client, ctx.decision_store, ctx.clock)

        return SetPlacementActionResult(result, self.name, self.action_id)

    async def set_placement_zones(
        self, client: KubeClient, store: DecisionStore, clock: Clock
    ) -> Union[bool, ErrorResponse]:
        result: Union[bool, ErrorResponse]
        timestamp = clock.now_seconds() * 1000
        try:
            new_placement_zones = [zone.id for zone in self.decision.placements]
            latest = await client.get(AnyApplication.GVK, self.name)
            if latest:
                app = AnyApplication(latest)
                uid = app.get_uid()
                current_zones = set(app.get_placement_zones())
                if current_zones == set(new_placement_zones):
                    logger.info("Current placement equals to new placement. Keeping placement unchanged.")
                    return True
                app.set_placement_zones(new_placement_zones)
                await client.patch_status(AnyApplication.GVK, self.name, app.get_status_or_fail())

                result = True
                logger.info(f"{self.name.to_string()}: setting placement zones done")

                # adding kube event
                await self.emit_event_or_fail_silently(client, timestamp, uid)

                # saving to decision store
                await self.store_decision(store, new_placement_zones, timestamp)
            else:
                logger.error(
                    f"{self.name.to_string()}: setting placement zones failure. Empty response from kube client."
                )
                result = ErrorResponse(status=500, code="INTERNAL_ERROR", msg="Empty response from kube client")
        except Exception as e:
            logger.error(f"{self.name.to_string()}: setting placement zones failure {str(e)}")
            result = ErrorResponse(status=500, code="INTERNAL_ERROR", msg=str(e))
        return result

    async def emit_event_or_fail_silently(self, client: KubeClient, timestamp: int, uid: Optional[str]) -> None:
        if uid is None:
            logger.warning("Not emitting event since uid is None")
            return
        try:
            zones = ", ".join([zone.id for zone in self.decision.placements])
            await client.emit_event(
                AnyApplication.GVK,
                self.name,
                uid,
                "SetPlacement",
                "SetPlacement",
                f"Setting placement zones {zones}",
                "Normal",
                timestamp,
            )
        except Exception as e:
            logger.error(f"{self.get_application_name()}: Unable to emit event {e}")

    async def store_decision(self, store: DecisionStore, zones: List[str], timestamp: int) -> None:
        try:
            await store.save(
                name=self.get_application_name(),
                spec=self.decision.spec,
                placement=zones,
                reason=self.decision.reason,
                trace=self.decision.trace,
                timestamp=timestamp,
            )
        except Exception as e:
            logger.error(f"{self.get_application_name()}: Error while saving the placement decision. {e}")
