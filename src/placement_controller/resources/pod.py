from typing import Any, Dict

from placement_controller.clients.k8s.resource import BaseResource


class Pod(BaseResource):
    def __init__(self, object: Dict[str, Any]):
        super().__init__(object)
