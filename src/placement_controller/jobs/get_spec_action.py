from typing import Union

from application_client import models
from application_client.api.default import get_application_spec

from placement_controller.api.model import ErrorResponse
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.jobs.types import Action, ActionId, ActionResult, ExecutorContext


class GetSpecResult(ActionResult):
    response: Union[models.ApplicationSpec, ErrorResponse]

    def __init__(
        self, response: Union[models.ApplicationSpec, ErrorResponse], name: NamespacedName, action_id: ActionId
    ):
        super().__init__(name, action_id)
        self.response = response

    def is_success(self) -> bool:
        return not isinstance(self.response, ErrorResponse)


class GetSpecAction(Action[GetSpecResult]):

    def __init__(self, name: NamespacedName, action_id: ActionId):
        super().__init__(name, action_id)

    async def run(self, ctx: ExecutorContext) -> GetSpecResult:
        api_response = await get_application_spec.asyncio(
            namespace=self.name.namespace, name=self.name.name, client=ctx.application_controller_client
        )
        if not api_response:
            response = ErrorResponse(status=500, code="INTERNAL_ERROR", msg="Received empty response")
        elif isinstance(api_response, models.ErrorResponse):
            response = ErrorResponse(status=api_response.status, code=api_response.code, msg=api_response.message)
        elif isinstance(api_response, models.ApplicationSpec):
            response = api_response  # type: ignore
        return GetSpecResult(response, self.name, self.action_id)
