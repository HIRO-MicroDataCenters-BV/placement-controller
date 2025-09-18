from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="WorkloadStatus")


@_attrs_define
class WorkloadStatus:
    """
    Attributes:
        kind (str):
        name (str):
        namespace (str):
        ready (bool):
        desired (int):
        available (int):
        unavailable (int):
        message (str):
    """

    kind: str
    name: str
    namespace: str
    ready: bool
    desired: int
    available: int
    unavailable: int
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind

        name = self.name

        namespace = self.namespace

        ready = self.ready

        desired = self.desired

        available = self.available

        unavailable = self.unavailable

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "name": name,
                "namespace": namespace,
                "ready": ready,
                "desired": desired,
                "available": available,
                "unavailable": unavailable,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = d.pop("kind")

        name = d.pop("name")

        namespace = d.pop("namespace")

        ready = d.pop("ready")

        desired = d.pop("desired")

        available = d.pop("available")

        unavailable = d.pop("unavailable")

        message = d.pop("message")

        workload_status = cls(
            kind=kind,
            name=name,
            namespace=namespace,
            ready=ready,
            desired=desired,
            available=available,
            unavailable=unavailable,
            message=message,
        )

        workload_status.additional_properties = d
        return workload_status

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
