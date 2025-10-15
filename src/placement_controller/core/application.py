from typing import Any, Dict, List, Optional

from dataclasses import dataclass
from enum import StrEnum

from placement_controller.clients.k8s.client import GroupVersionKind, NamespacedName


class GlobalState(StrEnum):
    UnknownGlobalState = "Unknown"
    NewGlobalState = "New"
    PlacementGlobalState = "Placement"
    OperationalGlobalState = "Operational"
    RelocationGlobalState = "Relocation"
    FailureGlobalState = "Failure"
    OwnershipTransferGlobalState = "OwnershipTransfer"


class PlacementStrategy(StrEnum):
    Global = "Global"
    Local = "Local"


@dataclass
class AnyApplicationCondition:
    last_transition_time: str
    msg: str
    reason: str
    retry_attempt: int
    status: str
    cond_type: str
    zone_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lastTransitionTime": self.last_transition_time,
            "msg": self.msg,
            "reason": self.reason,
            "retryAttempt": self.retry_attempt,
            "status": self.status,
            "type": self.cond_type,
            "zoneId": self.zone_id,
        }

    def copy_into(self, condition: Dict[str, Any]) -> None:
        condition.update(self.to_dict())


class AnyApplication:
    GVK: GroupVersionKind = GroupVersionKind("dcp.hiro.io", "v1", "AnyApplication")

    object: Dict[str, Any]

    def __init__(self, object: Dict[str, Any]):
        self.object = object

    def get_namespaced_name(self) -> NamespacedName:
        name = self.object["metadata"]["name"]
        namespace = self.object["metadata"]["namespace"]
        return NamespacedName(name, namespace)

    def get_uid(self) -> Optional[str]:
        metadata: Dict[str, str] = self.object["metadata"] or {}
        return metadata.get("uid")

    def get_spec(self) -> Dict[str, Any]:
        return self.object.get("spec") or {}

    def get_placement_strategy(self) -> PlacementStrategy:
        strategy = self.get_spec()["placementStrategy"] or {}
        placement_strategy_str = strategy.get("strategy") or "Local"
        return PlacementStrategy(placement_strategy_str)

    def get_owner_zone(self) -> Optional[str]:
        status = self.object.get("status") or {}
        ownership = status.get("ownership") or {}
        return ownership.get("owner")

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
        ownership = status.get("ownership")
        if not ownership:
            raise Exception("Application status missing ownership section.")

        ownership["placements"] = [{"zone": zone, "node-affinity": None} for zone in zones]

    def get_placement_zones(self) -> List[str]:
        status = self.object.get("status") or {}
        ownership = status.get("ownership") or {}
        placements = ownership.get("placements") or []
        return [placement["zone"] for placement in placements]

    def get_global_state(self) -> Optional[GlobalState]:
        status = self.object.get("status") or {}
        ownership = status.get("ownership") or {}
        state = ownership.get("state")
        return GlobalState(state) if state else None

    def set_owner_zone(self, owner: str) -> None:
        status: Optional[Dict[str, Any]] = self.object.get("status")
        if not status:
            raise Exception("status is not available")
        ownership = status.get("ownership")
        if not ownership:
            raise Exception("Application status missing ownership section")

        ownership["owner"] = owner
        ownership["epoch"] = ownership.get("epoch", 0) + 1

    def get_desired_replica(self) -> int:
        spec = self.get_spec() or {}
        return int(spec.get("zones") or "1")

    def set_placement_condition(self, zone_id: str, condition: AnyApplicationCondition) -> None:
        status = self.object.setdefault("status", dict())
        zones = status.setdefault("zones", [])

        zone: Optional[Dict[str, Any]] = [zone for zone in zones if zone.get("zoneId") == zone_id][0]
        if zone is None:
            zone = {"zoneId": zone_id, "version": 1, "conditions": []}
            zones.append(zone)

        conditions = zone.setdefault("conditions", [])
        existing: Optional[Dict[str, Any]] = [
            condition for condition in conditions if condition.get("") == condition.cond_type
        ][0]
        if existing:
            condition.copy_into(existing)
        else:
            conditions.append(condition.to_dict())

    def fail_if_none(self, value: Any, msg: str) -> None:
        if not value:
            raise Exception(msg)
