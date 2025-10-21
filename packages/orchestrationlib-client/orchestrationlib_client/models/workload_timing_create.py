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


T = TypeVar("T", bound="WorkloadTimingCreate")


@_attrs_define
class WorkloadTimingCreate:
    """Schema for creating a workload timing.

    Attributes:
        id (UUID):
        pod_name (str):
        namespace (str):
        node_name (str):
        scheduler_type (WorkloadTimingSchedulerEnum): Enum for workload timing schedulers.
        pod_uid (str):
        created_timestamp (Union[None, Unset, datetime.datetime]):
        scheduled_timestamp (Union[None, Unset, datetime.datetime]):
        ready_timestamp (Union[None, Unset, datetime.datetime]):
        deleted_timestamp (Union[None, Unset, datetime.datetime]):
        phase (Union[None, Unset, str]):
        reason (Union[None, Unset, str]):
        is_completed (Union[None, Unset, bool]):  Default: False.
        recorded_at (Union[None, Unset, datetime.datetime]):  Default: isoparse('2025-10-21T10:16:51.444307Z').
    """

    id: UUID
    pod_name: str
    namespace: str
    node_name: str
    scheduler_type: WorkloadTimingSchedulerEnum
    pod_uid: str
    created_timestamp: Union[None, Unset, datetime.datetime] = UNSET
    scheduled_timestamp: Union[None, Unset, datetime.datetime] = UNSET
    ready_timestamp: Union[None, Unset, datetime.datetime] = UNSET
    deleted_timestamp: Union[None, Unset, datetime.datetime] = UNSET
    phase: Union[None, Unset, str] = UNSET
    reason: Union[None, Unset, str] = UNSET
    is_completed: Union[None, Unset, bool] = False
    recorded_at: Union[None, Unset, datetime.datetime] = isoparse(
        "2025-10-21T10:16:51.444307Z"
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        pod_name = self.pod_name

        namespace = self.namespace

        node_name = self.node_name

        scheduler_type = self.scheduler_type.value

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
                "node_name": node_name,
                "scheduler_type": scheduler_type,
                "pod_uid": pod_uid,
            }
        )
        if created_timestamp is not UNSET:
            field_dict["created_timestamp"] = created_timestamp
        if scheduled_timestamp is not UNSET:
            field_dict["scheduled_timestamp"] = scheduled_timestamp
        if ready_timestamp is not UNSET:
            field_dict["ready_timestamp"] = ready_timestamp
        if deleted_timestamp is not UNSET:
            field_dict["deleted_timestamp"] = deleted_timestamp
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

        node_name = d.pop("node_name")

        scheduler_type = WorkloadTimingSchedulerEnum(d.pop("scheduler_type"))

        pod_uid = d.pop("pod_uid")

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

        workload_timing_create = cls(
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
            phase=phase,
            reason=reason,
            is_completed=is_completed,
            recorded_at=recorded_at,
        )

        workload_timing_create.additional_properties = d
        return workload_timing_create

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
