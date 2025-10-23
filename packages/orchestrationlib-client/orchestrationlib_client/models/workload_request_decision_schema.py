from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.pod_parent_type_enum import PodParentTypeEnum
from ..models.workload_action_type_enum import WorkloadActionTypeEnum
from ..models.workload_request_decision_status_enum import (
    WorkloadRequestDecisionStatusEnum,
)
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime


T = TypeVar("T", bound="WorkloadRequestDecisionSchema")


@_attrs_define
class WorkloadRequestDecisionSchema:
    """Schema for workload decision.

    Attributes:
        id (UUID):
        pod_id (UUID):
        pod_name (str):
        namespace (str):
        node_id (UUID):
        node_name (str):
        action_type (WorkloadActionTypeEnum): Enum for workload action types.
        decision_status (WorkloadRequestDecisionStatusEnum): Enum for workload request decision statuses.
        pod_parent_id (UUID):
        pod_parent_name (str):
        pod_parent_kind (PodParentTypeEnum): Enum for pod parent types.

        is_elastic (Union[None, Unset, bool]):
        queue_name (Union[None, Unset, str]):
        demand_cpu (Union[None, Unset, float]):
        demand_memory (Union[None, Unset, float]):
        demand_slack_cpu (Union[None, Unset, float]):
        demand_slack_memory (Union[None, Unset, float]):
        decision_start_time (Union[None, Unset, datetime.datetime]):
        decision_end_time (Union[None, Unset, datetime.datetime]):
        created_at (Union[None, Unset, datetime.datetime]):
        deleted_at (Union[None, Unset, datetime.datetime]):
    """

    id: UUID
    pod_id: UUID
    pod_name: str
    namespace: str
    node_id: UUID
    node_name: str
    action_type: WorkloadActionTypeEnum
    decision_status: WorkloadRequestDecisionStatusEnum
    pod_parent_id: UUID
    pod_parent_name: str
    pod_parent_kind: PodParentTypeEnum
    is_elastic: Union[None, Unset, bool] = UNSET
    queue_name: Union[None, Unset, str] = UNSET
    demand_cpu: Union[None, Unset, float] = UNSET
    demand_memory: Union[None, Unset, float] = UNSET
    demand_slack_cpu: Union[None, Unset, float] = UNSET
    demand_slack_memory: Union[None, Unset, float] = UNSET
    decision_start_time: Union[None, Unset, datetime.datetime] = UNSET
    decision_end_time: Union[None, Unset, datetime.datetime] = UNSET
    created_at: Union[None, Unset, datetime.datetime] = UNSET
    deleted_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        pod_id = str(self.pod_id)

        pod_name = self.pod_name

        namespace = self.namespace

        node_id = str(self.node_id)

        node_name = self.node_name

        action_type = self.action_type.value

        decision_status = self.decision_status.value

        pod_parent_id = str(self.pod_parent_id)

        pod_parent_name = self.pod_parent_name

        pod_parent_kind = self.pod_parent_kind.value

        is_elastic: Union[None, Unset, bool]
        if isinstance(self.is_elastic, Unset):
            is_elastic = UNSET
        else:
            is_elastic = self.is_elastic

        queue_name: Union[None, Unset, str]
        if isinstance(self.queue_name, Unset):
            queue_name = UNSET
        else:
            queue_name = self.queue_name

        demand_cpu: Union[None, Unset, float]
        if isinstance(self.demand_cpu, Unset):
            demand_cpu = UNSET
        else:
            demand_cpu = self.demand_cpu

        demand_memory: Union[None, Unset, float]
        if isinstance(self.demand_memory, Unset):
            demand_memory = UNSET
        else:
            demand_memory = self.demand_memory

        demand_slack_cpu: Union[None, Unset, float]
        if isinstance(self.demand_slack_cpu, Unset):
            demand_slack_cpu = UNSET
        else:
            demand_slack_cpu = self.demand_slack_cpu

        demand_slack_memory: Union[None, Unset, float]
        if isinstance(self.demand_slack_memory, Unset):
            demand_slack_memory = UNSET
        else:
            demand_slack_memory = self.demand_slack_memory

        decision_start_time: Union[None, Unset, str]
        if isinstance(self.decision_start_time, Unset):
            decision_start_time = UNSET
        elif isinstance(self.decision_start_time, datetime.datetime):
            decision_start_time = self.decision_start_time.isoformat()
        else:
            decision_start_time = self.decision_start_time

        decision_end_time: Union[None, Unset, str]
        if isinstance(self.decision_end_time, Unset):
            decision_end_time = UNSET
        elif isinstance(self.decision_end_time, datetime.datetime):
            decision_end_time = self.decision_end_time.isoformat()
        else:
            decision_end_time = self.decision_end_time

        created_at: Union[None, Unset, str]
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        deleted_at: Union[None, Unset, str]
        if isinstance(self.deleted_at, Unset):
            deleted_at = UNSET
        elif isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat()
        else:
            deleted_at = self.deleted_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "pod_id": pod_id,
                "pod_name": pod_name,
                "namespace": namespace,
                "node_id": node_id,
                "node_name": node_name,
                "action_type": action_type,
                "decision_status": decision_status,
                "pod_parent_id": pod_parent_id,
                "pod_parent_name": pod_parent_name,
                "pod_parent_kind": pod_parent_kind,
            }
        )
        if is_elastic is not UNSET:
            field_dict["is_elastic"] = is_elastic
        if queue_name is not UNSET:
            field_dict["queue_name"] = queue_name
        if demand_cpu is not UNSET:
            field_dict["demand_cpu"] = demand_cpu
        if demand_memory is not UNSET:
            field_dict["demand_memory"] = demand_memory
        if demand_slack_cpu is not UNSET:
            field_dict["demand_slack_cpu"] = demand_slack_cpu
        if demand_slack_memory is not UNSET:
            field_dict["demand_slack_memory"] = demand_slack_memory
        if decision_start_time is not UNSET:
            field_dict["decision_start_time"] = decision_start_time
        if decision_end_time is not UNSET:
            field_dict["decision_end_time"] = decision_end_time
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        pod_id = UUID(d.pop("pod_id"))

        pod_name = d.pop("pod_name")

        namespace = d.pop("namespace")

        node_id = UUID(d.pop("node_id"))

        node_name = d.pop("node_name")

        action_type = WorkloadActionTypeEnum(d.pop("action_type"))

        decision_status = WorkloadRequestDecisionStatusEnum(d.pop("decision_status"))

        pod_parent_id = UUID(d.pop("pod_parent_id"))

        pod_parent_name = d.pop("pod_parent_name")

        pod_parent_kind = PodParentTypeEnum(d.pop("pod_parent_kind"))

        def _parse_is_elastic(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_elastic = _parse_is_elastic(d.pop("is_elastic", UNSET))

        def _parse_queue_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        queue_name = _parse_queue_name(d.pop("queue_name", UNSET))

        def _parse_demand_cpu(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        demand_cpu = _parse_demand_cpu(d.pop("demand_cpu", UNSET))

        def _parse_demand_memory(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        demand_memory = _parse_demand_memory(d.pop("demand_memory", UNSET))

        def _parse_demand_slack_cpu(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        demand_slack_cpu = _parse_demand_slack_cpu(d.pop("demand_slack_cpu", UNSET))

        def _parse_demand_slack_memory(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        demand_slack_memory = _parse_demand_slack_memory(
            d.pop("demand_slack_memory", UNSET)
        )

        def _parse_decision_start_time(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                decision_start_time_type_0 = isoparse(data)

                return decision_start_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        decision_start_time = _parse_decision_start_time(
            d.pop("decision_start_time", UNSET)
        )

        def _parse_decision_end_time(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                decision_end_time_type_0 = isoparse(data)

                return decision_end_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        decision_end_time = _parse_decision_end_time(d.pop("decision_end_time", UNSET))

        def _parse_created_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_deleted_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deleted_at_type_0 = isoparse(data)

                return deleted_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        deleted_at = _parse_deleted_at(d.pop("deleted_at", UNSET))

        workload_request_decision_schema = cls(
            id=id,
            pod_id=pod_id,
            pod_name=pod_name,
            namespace=namespace,
            node_id=node_id,
            node_name=node_name,
            action_type=action_type,
            decision_status=decision_status,
            pod_parent_id=pod_parent_id,
            pod_parent_name=pod_parent_name,
            pod_parent_kind=pod_parent_kind,
            is_elastic=is_elastic,
            queue_name=queue_name,
            demand_cpu=demand_cpu,
            demand_memory=demand_memory,
            demand_slack_cpu=demand_slack_cpu,
            demand_slack_memory=demand_slack_memory,
            decision_start_time=decision_start_time,
            decision_end_time=decision_end_time,
            created_at=created_at,
            deleted_at=deleted_at,
        )

        workload_request_decision_schema.additional_properties = d
        return workload_request_decision_schema

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
