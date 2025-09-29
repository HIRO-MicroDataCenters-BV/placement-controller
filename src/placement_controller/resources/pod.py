from typing import Any, Dict, List, Optional

from decimal import Decimal

from kubernetes.utils.quantity import parse_quantity

from placement_controller.clients.k8s.resource import BaseResource


class Pod(BaseResource):
    def __init__(self, object: Dict[str, Any]):
        super().__init__(object)

    def get_node_name(self) -> Optional[str]:
        return self.object["spec"].get("nodeName")  # type: ignore

    def get_requests(self) -> List[Dict[str, Dict[str, Decimal]]]:
        return self.get_resources("requests")

    def get_limits(self) -> List[Dict[str, Dict[str, Decimal]]]:
        return self.get_resources("limits")

    def get_resources(self, resource_bound: str) -> List[Dict[str, Dict[str, Decimal]]]:
        spec = self.object.get("spec") or {}
        containers = spec.get("containers") or {}
        quantities: List[Dict[str, Dict[str, Decimal]]] = []
        for container in containers:
            name = container["name"]
            resources = container.get("resources") or {}
            requests = resources.get(resource_bound) or {}
            parsed = {resource: parse_quantity(q) for resource, q in requests.items()}
            quantities.append({name: parsed})
        return quantities
