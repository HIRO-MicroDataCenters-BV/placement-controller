from typing import Any, Dict, Optional

from placement_controller.clients.k8s.resource import BaseResource


class Pod(BaseResource):
    def __init__(self, object: Dict[str, Any]):
        super().__init__(object)

    def get_node_name(self) -> Optional[str]:
        return self.object["spec"].get("nodeName")  # type: ignore
