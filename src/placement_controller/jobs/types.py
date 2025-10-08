from typing import Generic, TypeVar

from dataclasses import dataclass

from application_client.client import Client

from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.zone.types import ZoneApiFactory

ActionId = str

DEFAULT_TIMEOUT_SECONDS = 10


# TODO dataclass
class ActionResult:
    name: NamespacedName
    action_id: ActionId

    def __init__(self, name: NamespacedName, action_id: ActionId):
        self.name = name
        self.action_id = action_id

    def get_application_name(self) -> NamespacedName:
        return self.name

    def get_id(self) -> ActionId:
        return self.action_id

    def is_success(self) -> bool:
        raise NotImplementedError


@dataclass
class ExecutorContext:
    application_controller_client: Client
    zone_api_factory: ZoneApiFactory


T = TypeVar("T", bound="ActionResult")


class Action(Generic[T]):
    action_id: ActionId
    name: NamespacedName

    def __init__(self, name: NamespacedName, action_id: ActionId):
        self.action_id = action_id
        self.name = name

    def get_application_name(self) -> NamespacedName:
        return self.name

    def get_id(self) -> ActionId:
        return self.action_id

    def get_timeout_seconds(self) -> int:
        return DEFAULT_TIMEOUT_SECONDS

    async def run(self, context: ExecutorContext) -> T:
        raise NotImplementedError()
