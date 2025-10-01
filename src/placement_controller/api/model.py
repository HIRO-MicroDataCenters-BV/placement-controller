from typing import List, Optional, Set

from enum import StrEnum

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


class BidCriteria(StrEnum):
    cpu = "cpu"
    memory = "memory"
    gpu = "nvidia.com/gpu"
    ephemeralStorage = "ephemeral-storage"
    pvcStorage = "storage"


class MetricUnit(StrEnum):
    core = "core"
    byte = "byte"
    watt = "watt"
    eur = "eur"


class Metric(StrEnum):
    cost = "cost"
    energy = "energy"

    def unit(self) -> MetricUnit:
        if self == Metric.cost:
            return MetricUnit.eur
        elif self == Metric.energy:
            return MetricUnit.watt
        else:
            raise Exception(f"We don't know the unit for metric {self}")


class BidRequestModel(BaseModel):
    id: str
    spec: str
    bid_criteria: List[BidCriteria]
    metrics: Set[Metric]


class BidStatus(StrEnum):
    accepted = "accepted"
    rejected = "rejected"


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
