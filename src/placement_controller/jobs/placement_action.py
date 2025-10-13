from typing import List, Optional, Union

from loguru import logger

from placement_controller.api.model import ErrorResponse
from placement_controller.clients.k8s.client import KubeClient, NamespacedName
from placement_controller.core.application import AnyApplication
from placement_controller.jobs.types import Action, ActionId, ActionResult, ExecutorContext
from placement_controller.membership.types import PlacementZone


class SetPlacementActionResult(ActionResult):
    result: Union[bool, ErrorResponse]

    def __init__(self, result: Union[bool, ErrorResponse], name: NamespacedName, action_id: ActionId):
        super().__init__(name, action_id)
        self.result = result

    def is_success(self) -> bool:
        return isinstance(self.result, ErrorResponse)


class SetPlacementAction(Action[SetPlacementActionResult]):
    zones: List[PlacementZone]

    def __init__(
        self,
        zones: List[PlacementZone],
        name: NamespacedName,
        action_id: ActionId,
    ):
        super().__init__(name, action_id)
        self.zones = zones

    async def run(self, ctx: ExecutorContext) -> SetPlacementActionResult:
        logger.info(f"{self.name.to_string()}: setting placement zones {self.zones}")

        result = await self.set_placement_zones(ctx.kube_client)

        return SetPlacementActionResult(result, self.name, self.action_id)

    async def set_placement_zones(self, client: KubeClient) -> Union[bool, ErrorResponse]:
        result: Union[bool, ErrorResponse]
        try:
            latest = await client.get(AnyApplication.GVK, self.name)
            if latest:
                app = AnyApplication(latest)
                uid = app.get_uid()
                app.set_placement_zones([zone.id for zone in self.zones])
                await client.patch_status(AnyApplication.GVK, self.name, app.get_status_or_fail())
                result = True
                logger.info(f"{self.name.to_string()}: setting placement zones done")
                await self.emit_event_or_fail_silently(client, uid)
            else:
                logger.error(
                    f"{self.name.to_string()}: setting placement zones failure. Empty response from kube client."
                )
                result = ErrorResponse(status=500, code="INTERNAL_ERROR", msg="Empty response from kube client")
        except Exception as e:
            logger.error(f"{self.name.to_string()}: setting placement zones failure {str(e)}")
            result = ErrorResponse(status=500, code="INTERNAL_ERROR", msg=str(e))
        return result

    async def emit_event_or_fail_silently(self, client: KubeClient, uid: Optional[str]) -> None:
        if uid is None:
            logger.warning("Not emitting event since uid is None")
            return

        zones = ", ".join([zone.id for zone in self.zones])
        await client.emit_event(
            AnyApplication.GVK,
            self.name,
            uid,
            "SetPlacement",
            "SetPlacement",
            f"Setting placement zones {zones}",
            "Normal",
            0,
        )
