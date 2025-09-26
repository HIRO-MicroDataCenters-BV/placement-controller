from typing import Any, Dict

from placement_controller.clients.k8s.resource import BaseResource


class Node(BaseResource):

    def __init__(self, object: Dict[str, Any]):
        super().__init__(object)

    def get_name(self) -> str:
        return self.object["metadata"]["name"]  # type: ignore
