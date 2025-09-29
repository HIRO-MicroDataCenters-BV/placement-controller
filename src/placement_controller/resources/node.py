from typing import Any, Dict

from decimal import Decimal

from kubernetes.utils.quantity import parse_quantity

from placement_controller.clients.k8s.resource import BaseResource


class Node(BaseResource):

    def __init__(self, object: Dict[str, Any]):
        super().__init__(object)

    def get_name(self) -> str:
        return self.object["metadata"]["name"]  # type: ignore

    def get_allocatable(self) -> Dict[str, Decimal]:
        status = self.object.get("status") or {}
        allocatable = status.get("allocatable") or {}
        quantities = {name: parse_quantity(q) for name, q in allocatable.items()}
        return quantities
