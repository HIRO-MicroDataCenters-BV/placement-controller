from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.workload_timing_scheduler_enum import WorkloadTimingSchedulerEnum
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime


T = TypeVar("T", bound="WorkloadTimingSchema")


@_attrs_define
class WorkloadTimingSchema:
    """Schema for workload timing.

    Attributes:
        id (UUID):
        pod_name (str):
        namespace (str):
        node_name (Union[None, Unset, str]):
        scheduler_type (Union[None, Unset, WorkloadTimingSchedulerEnum]):
        pod_uid (Union[None, Unset, str]):
        created_timestamp (Union[None, Unset, datetime.datetime]):
        scheduled_timestamp (Union[None, Unset, datetime.datetime]):
        ready_timestamp (Union[None, Unset, datetime.datetime]):
        deleted_timestamp (Union[None, Unset, datetime.datetime]):
        creation_to_scheduled_ms (Union[None, Unset, float]):
        scheduled_to_ready_ms (Union[None, Unset, float]):
        creation_to_ready_ms (Union[None, Unset, float]):
        total_lifecycle_ms (Union[None, Unset, float]):
        phase (Union[None, Unset, str]):
        reason (Union[None, Unset, str]):
        is_completed (Union[None, Unset, bool]):  Default: False.
        recorded_at (Union[None, Unset, datetime.datetime]):
    """

    id: UUID
    pod_name: str
    namespace: str
    node_name: Union[None, Unset, str] = UNSET
    scheduler_type: Union[None, Unset, WorkloadTimingSchedulerEnum] = UNSET
    pod_uid: Union[None, Unset, str] = UNSET
    created_timestamp: Union[None, Unset, datetime.datetime] = UNSET
    scheduled_timestamp: Union[None, Unset, datetime.datetime] = UNSET
    ready_timestamp: Union[None, Unset, datetime.datetime] = UNSET
    deleted_timestamp: Union[None, Unset, datetime.datetime] = UNSET
    creation_to_scheduled_ms: Union[None, Unset, float] = UNSET
    scheduled_to_ready_ms: Union[None, Unset, float] = UNSET
    creation_to_ready_ms: Union[None, Unset, float] = UNSET
    total_lifecycle_ms: Union[None, Unset, float] = UNSET
    phase: Union[None, Unset, str] = UNSET
    reason: Union[None, Unset, str] = UNSET
    is_completed: Union[None, Unset, bool] = False
    recorded_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        pod_name = self.pod_name

        namespace = self.namespace

        node_name: Union[None, Unset, str]
        if isinstance(self.node_name, Unset):
            node_name = UNSET
        else:
            node_name = self.node_name

        scheduler_type: Union[None, Unset, str]
        if isinstance(self.scheduler_type, Unset):
            scheduler_type = UNSET
        elif isinstance(self.scheduler_type, WorkloadTimingSchedulerEnum):
            scheduler_type = self.scheduler_type.value
        else:
            scheduler_type = self.scheduler_type

        pod_uid: Union[None, Unset, str]
        if isinstance(self.pod_uid, Unset):
            pod_uid = UNSET
        else:
            pod_uid = self.pod_uid

        created_timestamp: Union[None, Unset, str]
        if isinstance(self.created_timestamp, Unset):
            created_timestamp = UNSET
        elif isinstance(self.created_timestamp, datetime.datetime):
            created_timestamp = self.created_timestamp.isoformat()
        else:
            created_timestamp = self.created_timestamp

        scheduled_timestamp: Union[None, Unset, str]
        if isinstance(self.scheduled_timestamp, Unset):
            scheduled_timestamp = UNSET
        elif isinstance(self.scheduled_timestamp, datetime.datetime):
            scheduled_timestamp = self.scheduled_timestamp.isoformat()
        else:
            scheduled_timestamp = self.scheduled_timestamp

        ready_timestamp: Union[None, Unset, str]
        if isinstance(self.ready_timestamp, Unset):
            ready_timestamp = UNSET
        elif isinstance(self.ready_timestamp, datetime.datetime):
            ready_timestamp = self.ready_timestamp.isoformat()
        else:
            ready_timestamp = self.ready_timestamp

        deleted_timestamp: Union[None, Unset, str]
        if isinstance(self.deleted_timestamp, Unset):
            deleted_timestamp = UNSET
        elif isinstance(self.deleted_timestamp, datetime.datetime):
            deleted_timestamp = self.deleted_timestamp.isoformat()
        else:
            deleted_timestamp = self.deleted_timestamp

        creation_to_scheduled_ms: Union[None, Unset, float]
        if isinstance(self.creation_to_scheduled_ms, Unset):
            creation_to_scheduled_ms = UNSET
        else:
            creation_to_scheduled_ms = self.creation_to_scheduled_ms

        scheduled_to_ready_ms: Union[None, Unset, float]
        if isinstance(self.scheduled_to_ready_ms, Unset):
            scheduled_to_ready_ms = UNSET
        else:
            scheduled_to_ready_ms = self.scheduled_to_ready_ms

        creation_to_ready_ms: Union[None, Unset, float]
        if isinstance(self.creation_to_ready_ms, Unset):
            creation_to_ready_ms = UNSET
        else:
            creation_to_ready_ms = self.creation_to_ready_ms

        total_lifecycle_ms: Union[None, Unset, float]
        if isinstance(self.total_lifecycle_ms, Unset):
            total_lifecycle_ms = UNSET
        else:
            total_lifecycle_ms = self.total_lifecycle_ms

        phase: Union[None, Unset, str]
        if isinstance(self.phase, Unset):
            phase = UNSET
        else:
            phase = self.phase

        reason: Union[None, Unset, str]
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        is_completed: Union[None, Unset, bool]
        if isinstance(self.is_completed, Unset):
            is_completed = UNSET
        else:
            is_completed = self.is_completed

        recorded_at: Union[None, Unset, str]
        if isinstance(self.recorded_at, Unset):
            recorded_at = UNSET
        elif isinstance(self.recorded_at, datetime.datetime):
            recorded_at = self.recorded_at.isoformat()
        else:
            recorded_at = self.recorded_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "pod_name": pod_name,
                "namespace": namespace,
            }
        )
        if node_name is not UNSET:
            field_dict["node_name"] = node_name
        if scheduler_type is not UNSET:
            field_dict["scheduler_type"] = scheduler_type
        if pod_uid is not UNSET:
            field_dict["pod_uid"] = pod_uid
        if created_timestamp is not UNSET:
            field_dict["created_timestamp"] = created_timestamp
        if scheduled_timestamp is not UNSET:
            field_dict["scheduled_timestamp"] = scheduled_timestamp
        if ready_timestamp is not UNSET:
            field_dict["ready_timestamp"] = ready_timestamp
        if deleted_timestamp is not UNSET:
            field_dict["deleted_timestamp"] = deleted_timestamp
        if creation_to_scheduled_ms is not UNSET:
            field_dict["creation_to_scheduled_ms"] = creation_to_scheduled_ms
        if scheduled_to_ready_ms is not UNSET:
            field_dict["scheduled_to_ready_ms"] = scheduled_to_ready_ms
        if creation_to_ready_ms is not UNSET:
            field_dict["creation_to_ready_ms"] = creation_to_ready_ms
        if total_lifecycle_ms is not UNSET:
            field_dict["total_lifecycle_ms"] = total_lifecycle_ms
        if phase is not UNSET:
            field_dict["phase"] = phase
        if reason is not UNSET:
            field_dict["reason"] = reason
        if is_completed is not UNSET:
            field_dict["is_completed"] = is_completed
        if recorded_at is not UNSET:
            field_dict["recorded_at"] = recorded_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        pod_name = d.pop("pod_name")

        namespace = d.pop("namespace")

        def _parse_node_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        node_name = _parse_node_name(d.pop("node_name", UNSET))

        def _parse_scheduler_type(
            data: object,
        ) -> Union[None, Unset, WorkloadTimingSchedulerEnum]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scheduler_type_type_0 = WorkloadTimingSchedulerEnum(data)

                return scheduler_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, WorkloadTimingSchedulerEnum], data)

        scheduler_type = _parse_scheduler_type(d.pop("scheduler_type", UNSET))

        def _parse_pod_uid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pod_uid = _parse_pod_uid(d.pop("pod_uid", UNSET))

        def _parse_created_timestamp(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_timestamp_type_0 = isoparse(data)

                return created_timestamp_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        created_timestamp = _parse_created_timestamp(d.pop("created_timestamp", UNSET))

        def _parse_scheduled_timestamp(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scheduled_timestamp_type_0 = isoparse(data)

                return scheduled_timestamp_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        scheduled_timestamp = _parse_scheduled_timestamp(
            d.pop("scheduled_timestamp", UNSET)
        )

        def _parse_ready_timestamp(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ready_timestamp_type_0 = isoparse(data)

                return ready_timestamp_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        ready_timestamp = _parse_ready_timestamp(d.pop("ready_timestamp", UNSET))

        def _parse_deleted_timestamp(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deleted_timestamp_type_0 = isoparse(data)

                return deleted_timestamp_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        deleted_timestamp = _parse_deleted_timestamp(d.pop("deleted_timestamp", UNSET))

        def _parse_creation_to_scheduled_ms(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        creation_to_scheduled_ms = _parse_creation_to_scheduled_ms(
            d.pop("creation_to_scheduled_ms", UNSET)
        )

        def _parse_scheduled_to_ready_ms(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        scheduled_to_ready_ms = _parse_scheduled_to_ready_ms(
            d.pop("scheduled_to_ready_ms", UNSET)
        )

        def _parse_creation_to_ready_ms(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        creation_to_ready_ms = _parse_creation_to_ready_ms(
            d.pop("creation_to_ready_ms", UNSET)
        )

        def _parse_total_lifecycle_ms(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        total_lifecycle_ms = _parse_total_lifecycle_ms(
            d.pop("total_lifecycle_ms", UNSET)
        )

        def _parse_phase(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        phase = _parse_phase(d.pop("phase", UNSET))

        def _parse_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        reason = _parse_reason(d.pop("reason", UNSET))

        def _parse_is_completed(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_completed = _parse_is_completed(d.pop("is_completed", UNSET))

        def _parse_recorded_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                recorded_at_type_0 = isoparse(data)

                return recorded_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        recorded_at = _parse_recorded_at(d.pop("recorded_at", UNSET))

        workload_timing_schema = cls(
            id=id,
            pod_name=pod_name,
            namespace=namespace,
            node_name=node_name,
            scheduler_type=scheduler_type,
            pod_uid=pod_uid,
            created_timestamp=created_timestamp,
            scheduled_timestamp=scheduled_timestamp,
            ready_timestamp=ready_timestamp,
            deleted_timestamp=deleted_timestamp,
            creation_to_scheduled_ms=creation_to_scheduled_ms,
            scheduled_to_ready_ms=scheduled_to_ready_ms,
            creation_to_ready_ms=creation_to_ready_ms,
            total_lifecycle_ms=total_lifecycle_ms,
            phase=phase,
            reason=reason,
            is_completed=is_completed,
            recorded_at=recorded_at,
        )

        workload_timing_schema.additional_properties = d
        return workload_timing_schema

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
