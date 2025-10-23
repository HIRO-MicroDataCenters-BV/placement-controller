from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.workload_action_status_enum import WorkloadActionStatusEnum
from ..models.workload_action_type_enum import WorkloadActionTypeEnum
from ..models.workload_request_decision_status_enum import (
    WorkloadRequestDecisionStatusEnum,
)
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime


T = TypeVar("T", bound="WorkloadDecisionActionFlowItem")


@_attrs_define
class WorkloadDecisionActionFlowItem:
    """Schema for a single workload decision and action flow item.
    Matches columns from the workload_decision_action_flow view.

        Attributes:
            decision_id (UUID):
            action_id (UUID):
            action_type (WorkloadActionTypeEnum): Enum for workload action types.
            is_elastic (Union[None, Unset, bool]):
            queue_name (Union[None, Unset, str]):
            demand_cpu (Union[None, Unset, float]):
            demand_memory (Union[None, Unset, float]):
            demand_slack_cpu (Union[None, Unset, float]):
            demand_slack_memory (Union[None, Unset, float]):
            created_pod_name (Union[None, Unset, str]):
            created_pod_namespace (Union[None, Unset, str]):
            created_node_name (Union[None, Unset, str]):
            deleted_pod_name (Union[None, Unset, str]):
            deleted_pod_namespace (Union[None, Unset, str]):
            deleted_node_name (Union[None, Unset, str]):
            bound_pod_name (Union[None, Unset, str]):
            bound_pod_namespace (Union[None, Unset, str]):
            bound_node_name (Union[None, Unset, str]):
            decision_pod_name (Union[None, Unset, str]):
            decision_namespace (Union[None, Unset, str]):
            decision_node_name (Union[None, Unset, str]):
            decision_status (Union[None, Unset, WorkloadRequestDecisionStatusEnum]):
            action_status (Union[None, Unset, WorkloadActionStatusEnum]):
            decision_start_time (Union[None, Unset, datetime.datetime]):
            decision_end_time (Union[None, Unset, datetime.datetime]):
            action_start_time (Union[None, Unset, datetime.datetime]):
            action_end_time (Union[None, Unset, datetime.datetime]):
            decision_duration (Union[None, Unset, str]):
            action_duration (Union[None, Unset, str]):
            total_duration (Union[None, Unset, str]):
            decision_created_at (Union[None, Unset, datetime.datetime]):
            decision_deleted_at (Union[None, Unset, datetime.datetime]):
            action_created_at (Union[None, Unset, datetime.datetime]):
            action_updated_at (Union[None, Unset, datetime.datetime]):
            decision_pod_parent_id (Union[None, UUID, Unset]):
            decision_pod_parent_name (Union[None, Unset, str]):
            decision_pod_parent_kind (Union[None, Unset, str]):
            action_pod_parent_name (Union[None, Unset, str]):
            action_pod_parent_type (Union[None, Unset, str]):
            action_pod_parent_uid (Union[None, UUID, Unset]):
            action_reason (Union[None, Unset, str]):
    """

    decision_id: UUID
    action_id: UUID
    action_type: WorkloadActionTypeEnum
    is_elastic: Union[None, Unset, bool] = UNSET
    queue_name: Union[None, Unset, str] = UNSET
    demand_cpu: Union[None, Unset, float] = UNSET
    demand_memory: Union[None, Unset, float] = UNSET
    demand_slack_cpu: Union[None, Unset, float] = UNSET
    demand_slack_memory: Union[None, Unset, float] = UNSET
    created_pod_name: Union[None, Unset, str] = UNSET
    created_pod_namespace: Union[None, Unset, str] = UNSET
    created_node_name: Union[None, Unset, str] = UNSET
    deleted_pod_name: Union[None, Unset, str] = UNSET
    deleted_pod_namespace: Union[None, Unset, str] = UNSET
    deleted_node_name: Union[None, Unset, str] = UNSET
    bound_pod_name: Union[None, Unset, str] = UNSET
    bound_pod_namespace: Union[None, Unset, str] = UNSET
    bound_node_name: Union[None, Unset, str] = UNSET
    decision_pod_name: Union[None, Unset, str] = UNSET
    decision_namespace: Union[None, Unset, str] = UNSET
    decision_node_name: Union[None, Unset, str] = UNSET
    decision_status: Union[None, Unset, WorkloadRequestDecisionStatusEnum] = UNSET
    action_status: Union[None, Unset, WorkloadActionStatusEnum] = UNSET
    decision_start_time: Union[None, Unset, datetime.datetime] = UNSET
    decision_end_time: Union[None, Unset, datetime.datetime] = UNSET
    action_start_time: Union[None, Unset, datetime.datetime] = UNSET
    action_end_time: Union[None, Unset, datetime.datetime] = UNSET
    decision_duration: Union[None, Unset, str] = UNSET
    action_duration: Union[None, Unset, str] = UNSET
    total_duration: Union[None, Unset, str] = UNSET
    decision_created_at: Union[None, Unset, datetime.datetime] = UNSET
    decision_deleted_at: Union[None, Unset, datetime.datetime] = UNSET
    action_created_at: Union[None, Unset, datetime.datetime] = UNSET
    action_updated_at: Union[None, Unset, datetime.datetime] = UNSET
    decision_pod_parent_id: Union[None, UUID, Unset] = UNSET
    decision_pod_parent_name: Union[None, Unset, str] = UNSET
    decision_pod_parent_kind: Union[None, Unset, str] = UNSET
    action_pod_parent_name: Union[None, Unset, str] = UNSET
    action_pod_parent_type: Union[None, Unset, str] = UNSET
    action_pod_parent_uid: Union[None, UUID, Unset] = UNSET
    action_reason: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        decision_id = str(self.decision_id)

        action_id = str(self.action_id)

        action_type = self.action_type.value

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

        created_pod_name: Union[None, Unset, str]
        if isinstance(self.created_pod_name, Unset):
            created_pod_name = UNSET
        else:
            created_pod_name = self.created_pod_name

        created_pod_namespace: Union[None, Unset, str]
        if isinstance(self.created_pod_namespace, Unset):
            created_pod_namespace = UNSET
        else:
            created_pod_namespace = self.created_pod_namespace

        created_node_name: Union[None, Unset, str]
        if isinstance(self.created_node_name, Unset):
            created_node_name = UNSET
        else:
            created_node_name = self.created_node_name

        deleted_pod_name: Union[None, Unset, str]
        if isinstance(self.deleted_pod_name, Unset):
            deleted_pod_name = UNSET
        else:
            deleted_pod_name = self.deleted_pod_name

        deleted_pod_namespace: Union[None, Unset, str]
        if isinstance(self.deleted_pod_namespace, Unset):
            deleted_pod_namespace = UNSET
        else:
            deleted_pod_namespace = self.deleted_pod_namespace

        deleted_node_name: Union[None, Unset, str]
        if isinstance(self.deleted_node_name, Unset):
            deleted_node_name = UNSET
        else:
            deleted_node_name = self.deleted_node_name

        bound_pod_name: Union[None, Unset, str]
        if isinstance(self.bound_pod_name, Unset):
            bound_pod_name = UNSET
        else:
            bound_pod_name = self.bound_pod_name

        bound_pod_namespace: Union[None, Unset, str]
        if isinstance(self.bound_pod_namespace, Unset):
            bound_pod_namespace = UNSET
        else:
            bound_pod_namespace = self.bound_pod_namespace

        bound_node_name: Union[None, Unset, str]
        if isinstance(self.bound_node_name, Unset):
            bound_node_name = UNSET
        else:
            bound_node_name = self.bound_node_name

        decision_pod_name: Union[None, Unset, str]
        if isinstance(self.decision_pod_name, Unset):
            decision_pod_name = UNSET
        else:
            decision_pod_name = self.decision_pod_name

        decision_namespace: Union[None, Unset, str]
        if isinstance(self.decision_namespace, Unset):
            decision_namespace = UNSET
        else:
            decision_namespace = self.decision_namespace

        decision_node_name: Union[None, Unset, str]
        if isinstance(self.decision_node_name, Unset):
            decision_node_name = UNSET
        else:
            decision_node_name = self.decision_node_name

        decision_status: Union[None, Unset, str]
        if isinstance(self.decision_status, Unset):
            decision_status = UNSET
        elif isinstance(self.decision_status, WorkloadRequestDecisionStatusEnum):
            decision_status = self.decision_status.value
        else:
            decision_status = self.decision_status

        action_status: Union[None, Unset, str]
        if isinstance(self.action_status, Unset):
            action_status = UNSET
        elif isinstance(self.action_status, WorkloadActionStatusEnum):
            action_status = self.action_status.value
        else:
            action_status = self.action_status

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

        action_start_time: Union[None, Unset, str]
        if isinstance(self.action_start_time, Unset):
            action_start_time = UNSET
        elif isinstance(self.action_start_time, datetime.datetime):
            action_start_time = self.action_start_time.isoformat()
        else:
            action_start_time = self.action_start_time

        action_end_time: Union[None, Unset, str]
        if isinstance(self.action_end_time, Unset):
            action_end_time = UNSET
        elif isinstance(self.action_end_time, datetime.datetime):
            action_end_time = self.action_end_time.isoformat()
        else:
            action_end_time = self.action_end_time

        decision_duration: Union[None, Unset, str]
        if isinstance(self.decision_duration, Unset):
            decision_duration = UNSET
        else:
            decision_duration = self.decision_duration

        action_duration: Union[None, Unset, str]
        if isinstance(self.action_duration, Unset):
            action_duration = UNSET
        else:
            action_duration = self.action_duration

        total_duration: Union[None, Unset, str]
        if isinstance(self.total_duration, Unset):
            total_duration = UNSET
        else:
            total_duration = self.total_duration

        decision_created_at: Union[None, Unset, str]
        if isinstance(self.decision_created_at, Unset):
            decision_created_at = UNSET
        elif isinstance(self.decision_created_at, datetime.datetime):
            decision_created_at = self.decision_created_at.isoformat()
        else:
            decision_created_at = self.decision_created_at

        decision_deleted_at: Union[None, Unset, str]
        if isinstance(self.decision_deleted_at, Unset):
            decision_deleted_at = UNSET
        elif isinstance(self.decision_deleted_at, datetime.datetime):
            decision_deleted_at = self.decision_deleted_at.isoformat()
        else:
            decision_deleted_at = self.decision_deleted_at

        action_created_at: Union[None, Unset, str]
        if isinstance(self.action_created_at, Unset):
            action_created_at = UNSET
        elif isinstance(self.action_created_at, datetime.datetime):
            action_created_at = self.action_created_at.isoformat()
        else:
            action_created_at = self.action_created_at

        action_updated_at: Union[None, Unset, str]
        if isinstance(self.action_updated_at, Unset):
            action_updated_at = UNSET
        elif isinstance(self.action_updated_at, datetime.datetime):
            action_updated_at = self.action_updated_at.isoformat()
        else:
            action_updated_at = self.action_updated_at

        decision_pod_parent_id: Union[None, Unset, str]
        if isinstance(self.decision_pod_parent_id, Unset):
            decision_pod_parent_id = UNSET
        elif isinstance(self.decision_pod_parent_id, UUID):
            decision_pod_parent_id = str(self.decision_pod_parent_id)
        else:
            decision_pod_parent_id = self.decision_pod_parent_id

        decision_pod_parent_name: Union[None, Unset, str]
        if isinstance(self.decision_pod_parent_name, Unset):
            decision_pod_parent_name = UNSET
        else:
            decision_pod_parent_name = self.decision_pod_parent_name

        decision_pod_parent_kind: Union[None, Unset, str]
        if isinstance(self.decision_pod_parent_kind, Unset):
            decision_pod_parent_kind = UNSET
        else:
            decision_pod_parent_kind = self.decision_pod_parent_kind

        action_pod_parent_name: Union[None, Unset, str]
        if isinstance(self.action_pod_parent_name, Unset):
            action_pod_parent_name = UNSET
        else:
            action_pod_parent_name = self.action_pod_parent_name

        action_pod_parent_type: Union[None, Unset, str]
        if isinstance(self.action_pod_parent_type, Unset):
            action_pod_parent_type = UNSET
        else:
            action_pod_parent_type = self.action_pod_parent_type

        action_pod_parent_uid: Union[None, Unset, str]
        if isinstance(self.action_pod_parent_uid, Unset):
            action_pod_parent_uid = UNSET
        elif isinstance(self.action_pod_parent_uid, UUID):
            action_pod_parent_uid = str(self.action_pod_parent_uid)
        else:
            action_pod_parent_uid = self.action_pod_parent_uid

        action_reason: Union[None, Unset, str]
        if isinstance(self.action_reason, Unset):
            action_reason = UNSET
        else:
            action_reason = self.action_reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "decision_id": decision_id,
                "action_id": action_id,
                "action_type": action_type,
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
        if created_pod_name is not UNSET:
            field_dict["created_pod_name"] = created_pod_name
        if created_pod_namespace is not UNSET:
            field_dict["created_pod_namespace"] = created_pod_namespace
        if created_node_name is not UNSET:
            field_dict["created_node_name"] = created_node_name
        if deleted_pod_name is not UNSET:
            field_dict["deleted_pod_name"] = deleted_pod_name
        if deleted_pod_namespace is not UNSET:
            field_dict["deleted_pod_namespace"] = deleted_pod_namespace
        if deleted_node_name is not UNSET:
            field_dict["deleted_node_name"] = deleted_node_name
        if bound_pod_name is not UNSET:
            field_dict["bound_pod_name"] = bound_pod_name
        if bound_pod_namespace is not UNSET:
            field_dict["bound_pod_namespace"] = bound_pod_namespace
        if bound_node_name is not UNSET:
            field_dict["bound_node_name"] = bound_node_name
        if decision_pod_name is not UNSET:
            field_dict["decision_pod_name"] = decision_pod_name
        if decision_namespace is not UNSET:
            field_dict["decision_namespace"] = decision_namespace
        if decision_node_name is not UNSET:
            field_dict["decision_node_name"] = decision_node_name
        if decision_status is not UNSET:
            field_dict["decision_status"] = decision_status
        if action_status is not UNSET:
            field_dict["action_status"] = action_status
        if decision_start_time is not UNSET:
            field_dict["decision_start_time"] = decision_start_time
        if decision_end_time is not UNSET:
            field_dict["decision_end_time"] = decision_end_time
        if action_start_time is not UNSET:
            field_dict["action_start_time"] = action_start_time
        if action_end_time is not UNSET:
            field_dict["action_end_time"] = action_end_time
        if decision_duration is not UNSET:
            field_dict["decision_duration"] = decision_duration
        if action_duration is not UNSET:
            field_dict["action_duration"] = action_duration
        if total_duration is not UNSET:
            field_dict["total_duration"] = total_duration
        if decision_created_at is not UNSET:
            field_dict["decision_created_at"] = decision_created_at
        if decision_deleted_at is not UNSET:
            field_dict["decision_deleted_at"] = decision_deleted_at
        if action_created_at is not UNSET:
            field_dict["action_created_at"] = action_created_at
        if action_updated_at is not UNSET:
            field_dict["action_updated_at"] = action_updated_at
        if decision_pod_parent_id is not UNSET:
            field_dict["decision_pod_parent_id"] = decision_pod_parent_id
        if decision_pod_parent_name is not UNSET:
            field_dict["decision_pod_parent_name"] = decision_pod_parent_name
        if decision_pod_parent_kind is not UNSET:
            field_dict["decision_pod_parent_kind"] = decision_pod_parent_kind
        if action_pod_parent_name is not UNSET:
            field_dict["action_pod_parent_name"] = action_pod_parent_name
        if action_pod_parent_type is not UNSET:
            field_dict["action_pod_parent_type"] = action_pod_parent_type
        if action_pod_parent_uid is not UNSET:
            field_dict["action_pod_parent_uid"] = action_pod_parent_uid
        if action_reason is not UNSET:
            field_dict["action_reason"] = action_reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        decision_id = UUID(d.pop("decision_id"))

        action_id = UUID(d.pop("action_id"))

        action_type = WorkloadActionTypeEnum(d.pop("action_type"))

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

        def _parse_created_pod_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_pod_name = _parse_created_pod_name(d.pop("created_pod_name", UNSET))

        def _parse_created_pod_namespace(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_pod_namespace = _parse_created_pod_namespace(
            d.pop("created_pod_namespace", UNSET)
        )

        def _parse_created_node_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_node_name = _parse_created_node_name(d.pop("created_node_name", UNSET))

        def _parse_deleted_pod_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        deleted_pod_name = _parse_deleted_pod_name(d.pop("deleted_pod_name", UNSET))

        def _parse_deleted_pod_namespace(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        deleted_pod_namespace = _parse_deleted_pod_namespace(
            d.pop("deleted_pod_namespace", UNSET)
        )

        def _parse_deleted_node_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        deleted_node_name = _parse_deleted_node_name(d.pop("deleted_node_name", UNSET))

        def _parse_bound_pod_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        bound_pod_name = _parse_bound_pod_name(d.pop("bound_pod_name", UNSET))

        def _parse_bound_pod_namespace(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        bound_pod_namespace = _parse_bound_pod_namespace(
            d.pop("bound_pod_namespace", UNSET)
        )

        def _parse_bound_node_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        bound_node_name = _parse_bound_node_name(d.pop("bound_node_name", UNSET))

        def _parse_decision_pod_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        decision_pod_name = _parse_decision_pod_name(d.pop("decision_pod_name", UNSET))

        def _parse_decision_namespace(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        decision_namespace = _parse_decision_namespace(
            d.pop("decision_namespace", UNSET)
        )

        def _parse_decision_node_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        decision_node_name = _parse_decision_node_name(
            d.pop("decision_node_name", UNSET)
        )

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

        def _parse_action_status(
            data: object,
        ) -> Union[None, Unset, WorkloadActionStatusEnum]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_status_type_0 = WorkloadActionStatusEnum(data)

                return action_status_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, WorkloadActionStatusEnum], data)

        action_status = _parse_action_status(d.pop("action_status", UNSET))

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

        def _parse_action_start_time(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_start_time_type_0 = isoparse(data)

                return action_start_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        action_start_time = _parse_action_start_time(d.pop("action_start_time", UNSET))

        def _parse_action_end_time(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_end_time_type_0 = isoparse(data)

                return action_end_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        action_end_time = _parse_action_end_time(d.pop("action_end_time", UNSET))

        def _parse_decision_duration(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        decision_duration = _parse_decision_duration(d.pop("decision_duration", UNSET))

        def _parse_action_duration(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        action_duration = _parse_action_duration(d.pop("action_duration", UNSET))

        def _parse_total_duration(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        total_duration = _parse_total_duration(d.pop("total_duration", UNSET))

        def _parse_decision_created_at(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                decision_created_at_type_0 = isoparse(data)

                return decision_created_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        decision_created_at = _parse_decision_created_at(
            d.pop("decision_created_at", UNSET)
        )

        def _parse_decision_deleted_at(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                decision_deleted_at_type_0 = isoparse(data)

                return decision_deleted_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        decision_deleted_at = _parse_decision_deleted_at(
            d.pop("decision_deleted_at", UNSET)
        )

        def _parse_action_created_at(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_created_at_type_0 = isoparse(data)

                return action_created_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        action_created_at = _parse_action_created_at(d.pop("action_created_at", UNSET))

        def _parse_action_updated_at(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_updated_at_type_0 = isoparse(data)

                return action_updated_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        action_updated_at = _parse_action_updated_at(d.pop("action_updated_at", UNSET))

        def _parse_decision_pod_parent_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                decision_pod_parent_id_type_0 = UUID(data)

                return decision_pod_parent_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        decision_pod_parent_id = _parse_decision_pod_parent_id(
            d.pop("decision_pod_parent_id", UNSET)
        )

        def _parse_decision_pod_parent_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        decision_pod_parent_name = _parse_decision_pod_parent_name(
            d.pop("decision_pod_parent_name", UNSET)
        )

        def _parse_decision_pod_parent_kind(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        decision_pod_parent_kind = _parse_decision_pod_parent_kind(
            d.pop("decision_pod_parent_kind", UNSET)
        )

        def _parse_action_pod_parent_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        action_pod_parent_name = _parse_action_pod_parent_name(
            d.pop("action_pod_parent_name", UNSET)
        )

        def _parse_action_pod_parent_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        action_pod_parent_type = _parse_action_pod_parent_type(
            d.pop("action_pod_parent_type", UNSET)
        )

        def _parse_action_pod_parent_uid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_pod_parent_uid_type_0 = UUID(data)

                return action_pod_parent_uid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        action_pod_parent_uid = _parse_action_pod_parent_uid(
            d.pop("action_pod_parent_uid", UNSET)
        )

        def _parse_action_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        action_reason = _parse_action_reason(d.pop("action_reason", UNSET))

        workload_decision_action_flow_item = cls(
            decision_id=decision_id,
            action_id=action_id,
            action_type=action_type,
            is_elastic=is_elastic,
            queue_name=queue_name,
            demand_cpu=demand_cpu,
            demand_memory=demand_memory,
            demand_slack_cpu=demand_slack_cpu,
            demand_slack_memory=demand_slack_memory,
            created_pod_name=created_pod_name,
            created_pod_namespace=created_pod_namespace,
            created_node_name=created_node_name,
            deleted_pod_name=deleted_pod_name,
            deleted_pod_namespace=deleted_pod_namespace,
            deleted_node_name=deleted_node_name,
            bound_pod_name=bound_pod_name,
            bound_pod_namespace=bound_pod_namespace,
            bound_node_name=bound_node_name,
            decision_pod_name=decision_pod_name,
            decision_namespace=decision_namespace,
            decision_node_name=decision_node_name,
            decision_status=decision_status,
            action_status=action_status,
            decision_start_time=decision_start_time,
            decision_end_time=decision_end_time,
            action_start_time=action_start_time,
            action_end_time=action_end_time,
            decision_duration=decision_duration,
            action_duration=action_duration,
            total_duration=total_duration,
            decision_created_at=decision_created_at,
            decision_deleted_at=decision_deleted_at,
            action_created_at=action_created_at,
            action_updated_at=action_updated_at,
            decision_pod_parent_id=decision_pod_parent_id,
            decision_pod_parent_name=decision_pod_parent_name,
            decision_pod_parent_kind=decision_pod_parent_kind,
            action_pod_parent_name=action_pod_parent_name,
            action_pod_parent_type=action_pod_parent_type,
            action_pod_parent_uid=action_pod_parent_uid,
            action_reason=action_reason,
        )

        workload_decision_action_flow_item.additional_properties = d
        return workload_decision_action_flow_item

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
