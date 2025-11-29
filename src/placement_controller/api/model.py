from typing import List, Optional, Set

from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel

from placement_controller.core.application import AnyApplication


class ApplicationModel(BaseModel):
    name: str
    namespace: str
    owner: str
    zones: List[str]

    @staticmethod
    def from_object(application: AnyApplication) -> "ApplicationModel":
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

    def is_minimize(self) -> bool:
        if self == Metric.cost:
            return True
        elif self == Metric.energy:
            return True
        else:
            raise Exception(f"We don't know the is_max_better for metric {self}")


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
    value: Decimal
    unit: MetricUnit


class BidResponseModel(BaseModel):
    id: str
    status: BidStatus
    reason: Optional[str] = None
    msg: Optional[str] = None
    metrics: List[MetricValue]

    def get_metric_value(self, metric: Metric) -> Optional[MetricValue]:
        found = [m for m in self.metrics if m.id == metric]
        return next(iter(found), None)

    def to_human_readable(self) -> str:
        response_str = f"status={self.status}"
        if self.reason is not None:
            response_str = response_str + f", reason='{self.reason}'"
        if self.msg is not None:
            response_str = response_str + f", msg='{self.msg}'"
        if len(self.metrics) > 0:
            sep = ""
            response_str = response_str + ", metrics{ "
            for metric in self.metrics:
                response_str = response_str + sep + f"{metric.id}={metric.value} ({metric.unit})"
                sep = ", "
            response_str = response_str + "}"
        return response_str


class ErrorResponse(BaseModel):
    status: int
    code: str
    msg: Optional[str] = None

    def to_human_readable(self) -> str:
        response_str = f"error: code={self.code}, status={self.status}'"
        if self.msg is not None:
            response_str = response_str + f", msg='{self.msg}'"
        return response_str


class SchedulingEntry(BaseModel):
    seq_nr: int
    state: str
    msg: Optional[str]
    running_jobs: List[str]


class ApplicationState(BaseModel):
    name: str
    namespace: str
    history: List[SchedulingEntry]
