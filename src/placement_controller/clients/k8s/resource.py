from typing import Any, Dict

from placement_controller.clients.k8s.client import NamespacedName


class BaseResource:
    object: Dict[str, Any]

    def __init__(self, object: Dict[str, Any]):
        self.object = object

    def get_namespaced_name(self) -> NamespacedName:
        name = self.object["metadata"]["name"]
        namespace = self.object["metadata"]["namespace"]
        return NamespacedName(name, namespace)
