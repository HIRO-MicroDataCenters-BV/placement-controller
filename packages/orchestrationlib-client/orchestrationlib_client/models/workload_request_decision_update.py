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


T = TypeVar("T", bound="WorkloadRequestDecisionUpdate")


@_attrs_define
class WorkloadRequestDecisionUpdate:
    """Schema for workload update decision.

    Attributes:
        is_elastic (Union[None, Unset, bool]):
        queue_name (Union[None, Unset, str]):
        demand_cpu (Union[None, Unset, float]):
        demand_memory (Union[None, Unset, float]):
        demand_slack_cpu (Union[None, Unset, float]):
        demand_slack_memory (Union[None, Unset, float]):
        pod_name (Union[None, Unset, str]):
        namespace (Union[None, Unset, str]):
        node_id (Union[None, UUID, Unset]):
        node_name (Union[None, Unset, str]):
        action_type (Union[None, Unset, WorkloadActionTypeEnum]):
        decision_status (Union[None, Unset, WorkloadRequestDecisionStatusEnum]):
        pod_parent_id (Union[None, UUID, Unset]):
        pod_parent_name (Union[None, Unset, str]):
        pod_parent_kind (Union[None, PodParentTypeEnum, Unset]):
        decision_start_time (Union[None, Unset, datetime.datetime]):
        decision_end_time (Union[None, Unset, datetime.datetime]):
        deleted_at (Union[None, Unset, datetime.datetime]):
    """

    is_elastic: Union[None, Unset, bool] = UNSET
    queue_name: Union[None, Unset, str] = UNSET
    demand_cpu: Union[None, Unset, float] = UNSET
    demand_memory: Union[None, Unset, float] = UNSET
    demand_slack_cpu: Union[None, Unset, float] = UNSET
    demand_slack_memory: Union[None, Unset, float] = UNSET
    pod_name: Union[None, Unset, str] = UNSET
    namespace: Union[None, Unset, str] = UNSET
    node_id: Union[None, UUID, Unset] = UNSET
    node_name: Union[None, Unset, str] = UNSET
    action_type: Union[None, Unset, WorkloadActionTypeEnum] = UNSET
    decision_status: Union[None, Unset, WorkloadRequestDecisionStatusEnum] = UNSET
    pod_parent_id: Union[None, UUID, Unset] = UNSET
    pod_parent_name: Union[None, Unset, str] = UNSET
    pod_parent_kind: Union[None, PodParentTypeEnum, Unset] = UNSET
    decision_start_time: Union[None, Unset, datetime.datetime] = UNSET
    decision_end_time: Union[None, Unset, datetime.datetime] = UNSET
    deleted_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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

        pod_name: Union[None, Unset, str]
        if isinstance(self.pod_name, Unset):
            pod_name = UNSET
        else:
            pod_name = self.pod_name

        namespace: Union[None, Unset, str]
        if isinstance(self.namespace, Unset):
            namespace = UNSET
        else:
            namespace = self.namespace

        node_id: Union[None, Unset, str]
        if isinstance(self.node_id, Unset):
            node_id = UNSET
        elif isinstance(self.node_id, UUID):
            node_id = str(self.node_id)
        else:
            node_id = self.node_id

        node_name: Union[None, Unset, str]
        if isinstance(self.node_name, Unset):
            node_name = UNSET
        else:
            node_name = self.node_name

        action_type: Union[None, Unset, str]
        if isinstance(self.action_type, Unset):
            action_type = UNSET
        elif isinstance(self.action_type, WorkloadActionTypeEnum):
            action_type = self.action_type.value
        else:
            action_type = self.action_type

        decision_status: Union[None, Unset, str]
        if isinstance(self.decision_status, Unset):
            decision_status = UNSET
        elif isinstance(self.decision_status, WorkloadRequestDecisionStatusEnum):
            decision_status = self.decision_status.value
        else:
            decision_status = self.decision_status

        pod_parent_id: Union[None, Unset, str]
        if isinstance(self.pod_parent_id, Unset):
            pod_parent_id = UNSET
        elif isinstance(self.pod_parent_id, UUID):
            pod_parent_id = str(self.pod_parent_id)
        else:
            pod_parent_id = self.pod_parent_id

        pod_parent_name: Union[None, Unset, str]
        if isinstance(self.pod_parent_name, Unset):
            pod_parent_name = UNSET
        else:
            pod_parent_name = self.pod_parent_name

        pod_parent_kind: Union[None, Unset, str]
        if isinstance(self.pod_parent_kind, Unset):
            pod_parent_kind = UNSET
        elif isinstance(self.pod_parent_kind, PodParentTypeEnum):
            pod_parent_kind = self.pod_parent_kind.value
        else:
            pod_parent_kind = self.pod_parent_kind

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

        deleted_at: Union[None, Unset, str]
        if isinstance(self.deleted_at, Unset):
            deleted_at = UNSET
        elif isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat()
        else:
            deleted_at = self.deleted_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
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
        if pod_name is not UNSET:
            field_dict["pod_name"] = pod_name
        if namespace is not UNSET:
            field_dict["namespace"] = namespace
        if node_id is not UNSET:
            field_dict["node_id"] = node_id
        if node_name is not UNSET:
            field_dict["node_name"] = node_name
        if action_type is not UNSET:
            field_dict["action_type"] = action_type
        if decision_status is not UNSET:
            field_dict["decision_status"] = decision_status
        if pod_parent_id is not UNSET:
            field_dict["pod_parent_id"] = pod_parent_id
        if pod_parent_name is not UNSET:
            field_dict["pod_parent_name"] = pod_parent_name
        if pod_parent_kind is not UNSET:
            field_dict["pod_parent_kind"] = pod_parent_kind
        if decision_start_time is not UNSET:
            field_dict["decision_start_time"] = decision_start_time
        if decision_end_time is not UNSET:
            field_dict["decision_end_time"] = decision_end_time
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

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

        def _parse_pod_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pod_name = _parse_pod_name(d.pop("pod_name", UNSET))

        def _parse_namespace(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        namespace = _parse_namespace(d.pop("namespace", UNSET))

        def _parse_node_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                node_id_type_0 = UUID(data)

                return node_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        node_id = _parse_node_id(d.pop("node_id", UNSET))

        def _parse_node_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        node_name = _parse_node_name(d.pop("node_name", UNSET))

        def _parse_action_type(
            data: object,
        ) -> Union[None, Unset, WorkloadActionTypeEnum]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_type_type_0 = WorkloadActionTypeEnum(data)

                return action_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, WorkloadActionTypeEnum], data)

        action_type = _parse_action_type(d.pop("action_type", UNSET))

        def _parse_decision_status(
            data: object,
        ) -> Union[None, Unset, WorkloadRequestDecisionStatusEnum]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                decision_status_type_0 = WorkloadRequestDecisionStatusEnum(data)

                return decision_status_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, WorkloadRequestDecisionStatusEnum], data)

        decision_status = _parse_decision_status(d.pop("decision_status", UNSET))

        def _parse_pod_parent_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pod_parent_id_type_0 = UUID(data)

                return pod_parent_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        pod_parent_id = _parse_pod_parent_id(d.pop("pod_parent_id", UNSET))

        def _parse_pod_parent_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pod_parent_name = _parse_pod_parent_name(d.pop("pod_parent_name", UNSET))

        def _parse_pod_parent_kind(
            data: object,
        ) -> Union[None, PodParentTypeEnum, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pod_parent_kind_type_0 = PodParentTypeEnum(data)

                return pod_parent_kind_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, PodParentTypeEnum, Unset], data)

        pod_parent_kind = _parse_pod_parent_kind(d.pop("pod_parent_kind", UNSET))

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

        workload_request_decision_update = cls(
            is_elastic=is_elastic,
            queue_name=queue_name,
            demand_cpu=demand_cpu,
            demand_memory=demand_memory,
            demand_slack_cpu=demand_slack_cpu,
            demand_slack_memory=demand_slack_memory,
            pod_name=pod_name,
            namespace=namespace,
            node_id=node_id,
            node_name=node_name,
            action_type=action_type,
            decision_status=decision_status,
            pod_parent_id=pod_parent_id,
            pod_parent_name=pod_parent_name,
            pod_parent_kind=pod_parent_kind,
            decision_start_time=decision_start_time,
            decision_end_time=decision_end_time,
            deleted_at=deleted_at,
        )

        workload_request_decision_update.additional_properties = d
        return workload_request_decision_update

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
