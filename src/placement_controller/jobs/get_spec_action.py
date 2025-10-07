from typing import Union

from application_client import models
from application_client.api.default import get_application_spec
from application_client.client import Client

from placement_controller.api.model import ErrorResponse
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.jobs.types import Action, ActionId, ActionResult


class GetSpecResult(ActionResult):
    response: Union[models.ApplicationSpec, ErrorResponse]

    def __init__(
        self, response: Union[models.ApplicationSpec, ErrorResponse], name: NamespacedName, action_id: ActionId
    ):
        super().__init__(name, action_id)
        self.response = response


class GetSpecAction(Action[GetSpecResult]):
    client: Client

    def __init__(self, client: Client, name: NamespacedName, action_id: ActionId):
        super().__init__(name, action_id)
        self.client = client

    async def run(self) -> GetSpecResult:
        api_response = await get_application_spec.asyncio(
            namespace=self.name.namespace, name=self.name.name, client=self.client
        )
        if not api_response:
            response = ErrorResponse(status=500, code="INTERNAL_ERROR", msg="Received empty response")
        elif isinstance(api_response, models.ErrorResponse):
            response = ErrorResponse(status=api_response.status, code=api_response.code, msg=api_response.message)
        elif isinstance(api_response, models.ApplicationSpec):
            response = api_response  # type: ignore
        return GetSpecResult(response, self.name, self.action_id)
