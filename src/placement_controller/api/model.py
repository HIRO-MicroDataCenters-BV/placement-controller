from typing import List, Optional, Set

from enum import Enum

from pydantic import BaseModel

from placement_controller.core.application import Application


class ApplicationModel(BaseModel):
    name: str
    namespace: str
    owner: str
    zones: List[str]

    @staticmethod
    def from_object(application: Application) -> "ApplicationModel":
        name = application.get_namespaced_name()
        zones = application.get_placement_zones()
        owner = application.get_owner_zone() or ""
        return ApplicationModel(name=name.name, namespace=name.namespace, zones=zones, owner=owner)


class BidCriteria(str, Enum):
    cpu = "cpu"
    gpu = "gpu"
    ram = "ram"
    ephemeralStorage = "ephemeral-storage"
    pvcStorage = "pvc-storage"


class Metric(str, Enum):
    cost = "cost"
    energy = "energy"


class BidRequestModel(BaseModel):
    id: str
    spec: str
    bid_criteria: Set[BidCriteria]
    metrics: Set[Metric]


class BidStatus(str, Enum):
    accepted = "accepted"
    rejected = "rejected"


class MetricUnit(str, Enum):
    core = "core"
    byte = "byte"
    watt = "watt"
    eur = "eur"


class MetricValue(BaseModel):
    id: Metric
    value: str
    unit: MetricUnit


class BidResponseModel(BaseModel):
    id: str
    status: BidStatus
    reason: Optional[str] = None
    msg: Optional[str] = None
    metrics: List[MetricValue]


class ErrorResponse(BaseModel):
    status: int
    code: str
    msg: Optional[str] = None
