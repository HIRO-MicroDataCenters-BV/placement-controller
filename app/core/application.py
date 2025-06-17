from typing import Any, Dict, List, Optional

from app.clients.k8s.client import NamespacedName


class Application:
    object: Dict[str, Any]

    def __init__(self, object: Dict[str, Any]):
        self.object = object

    def get_namespaced_name(self) -> NamespacedName:
        name = self.object["metadata"]["name"]
        namespace = self.object["metadata"]["namespace"]
        return NamespacedName(name, namespace)

    def get_spec(self) -> Dict[str, Any]:
        return self.object.get("spec") or {}

    def get_owner_zone(self) -> Optional[str]:
        status = self.object.get("status") or {}
        return status.get("owner")

    def get_status_or_fail(self) -> Dict[str, Any]:
        status = self.get_status()
        if not status:
            raise Exception("status is not set")
        return status

    def get_status(self) -> Optional[Dict[str, Any]]:
        status = self.object.get("status")
        if not status:
            return None
        return {"status": status}

    def set_placement_zones(self, zones: List[str]) -> None:
        status: Optional[Dict[str, Any]] = self.object.get("status")
        if not status:
            raise Exception("status is not available")

        status["placements"] = [{"zone": zone, "node-affinity": None} for zone in zones]

    def get_placement_zones(self) -> List[str]:
        status = self.object.get("status") or {}
        placements = status.get("placements") or []
        return [placement["zone"] for placement in placements]

    def set_owner_zone(self, owner: str) -> None:
        status: Optional[Dict[str, Any]] = self.object.get("status")
        if not status:
            raise Exception("status is not available")

        status["owner"] = owner

    def fail_if_none(self, value: Any, msg: str) -> None:
        if not value:
            raise Exception(msg)
