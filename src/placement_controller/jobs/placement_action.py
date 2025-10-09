from typing import List, Union

from placement_controller.api.model import ErrorResponse
from placement_controller.clients.k8s.client import NamespacedName
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
        result: Union[bool, ErrorResponse]
        try:
            latest = await ctx.kube_client.get(AnyApplication.GVK, self.name)
            if latest:
                app = AnyApplication(latest)
                app.set_placement_zones([zone.id for zone in self.zones])
                await ctx.kube_client.patch_status(AnyApplication.GVK, self.name, app.get_status_or_fail())
                result = True
            else:
                result = ErrorResponse(status=500, code="INTERNAL_ERROR", msg="Empty response from kube client")
        except Exception as e:
            result = ErrorResponse(status=500, code="INTERNAL_ERROR", msg=str(e))

        return SetPlacementActionResult(result, self.name, self.action_id)
