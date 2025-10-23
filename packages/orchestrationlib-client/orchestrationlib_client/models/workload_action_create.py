from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.pod_parent_type_enum import PodParentTypeEnum
from ..models.workload_action_status_enum import WorkloadActionStatusEnum
from ..models.workload_action_type_enum import WorkloadActionTypeEnum
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime


T = TypeVar("T", bound="WorkloadActionCreate")


@_attrs_define
class WorkloadActionCreate:
    """Schema for creating a workload action.

    Attributes:
        created_pod_name (Union[None, Unset, str]):
        created_pod_namespace (Union[None, Unset, str]):
        created_node_name (Union[None, Unset, str]):
        deleted_pod_name (Union[None, Unset, str]):
        deleted_pod_namespace (Union[None, Unset, str]):
        deleted_node_name (Union[None, Unset, str]):
        bound_pod_name (Union[None, Unset, str]):
        bound_pod_namespace (Union[None, Unset, str]):
        bound_node_name (Union[None, Unset, str]):
        action_type (Union[Unset, WorkloadActionTypeEnum]): Enum for workload action types.
        action_status (Union[Unset, WorkloadActionStatusEnum]): Enum for action statuses.
        action_start_time (Union[None, Unset, datetime.datetime]):
        action_end_time (Union[None, Unset, datetime.datetime]):
        action_reason (Union[None, Unset, str]):
        pod_parent_name (Union[None, Unset, str]):
        pod_parent_type (Union[None, PodParentTypeEnum, Unset]):  Default: PodParentTypeEnum.DEPLOYMENT.
        pod_parent_uid (Union[None, UUID, Unset]):
        created_at (Union[None, Unset, datetime.datetime]):
        updated_at (Union[None, Unset, datetime.datetime]):
    """

    created_pod_name: Union[None, Unset, str] = UNSET
    created_pod_namespace: Union[None, Unset, str] = UNSET
    created_node_name: Union[None, Unset, str] = UNSET
    deleted_pod_name: Union[None, Unset, str] = UNSET
    deleted_pod_namespace: Union[None, Unset, str] = UNSET
    deleted_node_name: Union[None, Unset, str] = UNSET
    bound_pod_name: Union[None, Unset, str] = UNSET
    bound_pod_namespace: Union[None, Unset, str] = UNSET
    bound_node_name: Union[None, Unset, str] = UNSET
    action_type: Union[Unset, WorkloadActionTypeEnum] = UNSET
    action_status: Union[Unset, WorkloadActionStatusEnum] = UNSET
    action_start_time: Union[None, Unset, datetime.datetime] = UNSET
    action_end_time: Union[None, Unset, datetime.datetime] = UNSET
    action_reason: Union[None, Unset, str] = UNSET
    pod_parent_name: Union[None, Unset, str] = UNSET
    pod_parent_type: Union[None, PodParentTypeEnum, Unset] = (
        PodParentTypeEnum.DEPLOYMENT
    )
    pod_parent_uid: Union[None, UUID, Unset] = UNSET
    created_at: Union[None, Unset, datetime.datetime] = UNSET
    updated_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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

        action_type: Union[Unset, str] = UNSET
        if not isinstance(self.action_type, Unset):
            action_type = self.action_type.value

        action_status: Union[Unset, str] = UNSET
        if not isinstance(self.action_status, Unset):
            action_status = self.action_status.value

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

        action_reason: Union[None, Unset, str]
        if isinstance(self.action_reason, Unset):
            action_reason = UNSET
        else:
            action_reason = self.action_reason

        pod_parent_name: Union[None, Unset, str]
        if isinstance(self.pod_parent_name, Unset):
            pod_parent_name = UNSET
        else:
            pod_parent_name = self.pod_parent_name

        pod_parent_type: Union[None, Unset, str]
        if isinstance(self.pod_parent_type, Unset):
            pod_parent_type = UNSET
        elif isinstance(self.pod_parent_type, PodParentTypeEnum):
            pod_parent_type = self.pod_parent_type.value
        else:
            pod_parent_type = self.pod_parent_type

        pod_parent_uid: Union[None, Unset, str]
        if isinstance(self.pod_parent_uid, Unset):
            pod_parent_uid = UNSET
        elif isinstance(self.pod_parent_uid, UUID):
            pod_parent_uid = str(self.pod_parent_uid)
        else:
            pod_parent_uid = self.pod_parent_uid

        created_at: Union[None, Unset, str]
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: Union[None, Unset, str]
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
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
        if action_type is not UNSET:
            field_dict["action_type"] = action_type
        if action_status is not UNSET:
            field_dict["action_status"] = action_status
        if action_start_time is not UNSET:
            field_dict["action_start_time"] = action_start_time
        if action_end_time is not UNSET:
            field_dict["action_end_time"] = action_end_time
        if action_reason is not UNSET:
            field_dict["action_reason"] = action_reason
        if pod_parent_name is not UNSET:
            field_dict["pod_parent_name"] = pod_parent_name
        if pod_parent_type is not UNSET:
            field_dict["pod_parent_type"] = pod_parent_type
        if pod_parent_uid is not UNSET:
            field_dict["pod_parent_uid"] = pod_parent_uid
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

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

        _action_type = d.pop("action_type", UNSET)
        action_type: Union[Unset, WorkloadActionTypeEnum]
        if isinstance(_action_type, Unset):
            action_type = UNSET
        else:
            action_type = WorkloadActionTypeEnum(_action_type)

        _action_status = d.pop("action_status", UNSET)
        action_status: Union[Unset, WorkloadActionStatusEnum]
        if isinstance(_action_status, Unset):
            action_status = UNSET
        else:
            action_status = WorkloadActionStatusEnum(_action_status)

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

        def _parse_action_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        action_reason = _parse_action_reason(d.pop("action_reason", UNSET))

        def _parse_pod_parent_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pod_parent_name = _parse_pod_parent_name(d.pop("pod_parent_name", UNSET))

        def _parse_pod_parent_type(
            data: object,
        ) -> Union[None, PodParentTypeEnum, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pod_parent_type_type_0 = PodParentTypeEnum(data)

                return pod_parent_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, PodParentTypeEnum, Unset], data)

        pod_parent_type = _parse_pod_parent_type(d.pop("pod_parent_type", UNSET))

        def _parse_pod_parent_uid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pod_parent_uid_type_0 = UUID(data)

                return pod_parent_uid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        pod_parent_uid = _parse_pod_parent_uid(d.pop("pod_parent_uid", UNSET))

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

        def _parse_updated_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        workload_action_create = cls(
            created_pod_name=created_pod_name,
            created_pod_namespace=created_pod_namespace,
            created_node_name=created_node_name,
            deleted_pod_name=deleted_pod_name,
            deleted_pod_namespace=deleted_pod_namespace,
            deleted_node_name=deleted_node_name,
            bound_pod_name=bound_pod_name,
            bound_pod_namespace=bound_pod_namespace,
            bound_node_name=bound_node_name,
            action_type=action_type,
            action_status=action_status,
            action_start_time=action_start_time,
            action_end_time=action_end_time,
            action_reason=action_reason,
            pod_parent_name=pod_parent_name,
            pod_parent_type=pod_parent_type,
            pod_parent_uid=pod_parent_uid,
            created_at=created_at,
            updated_at=updated_at,
        )

        workload_action_create.additional_properties = d
        return workload_action_create

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
