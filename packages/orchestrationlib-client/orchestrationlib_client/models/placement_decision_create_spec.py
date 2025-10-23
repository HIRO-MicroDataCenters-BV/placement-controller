from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="PlacementDecisionCreateSpec")


@_attrs_define
class PlacementDecisionCreateSpec:
    """Arbitrary spec JSON (free-form). Contains resources list.

    Example:
        {'resources': [{'id': {'name': 'name', 'namespace': 'ns'}, 'limits': {'cpu': '1', 'ephemeral-storage': '1g',
            'ram': '3'}, 'replicas': 2, 'requests': {'cpu': '1', 'nvidia/gpu': '1', 'ram': '3'}, 'type': 'pod'}, {'id':
            {'name': 'name', 'namespace': 'ns'}, 'replicas': 2, 'size': '1G', 'storageClass': 'default', 'type': 'pvc'}]}

    """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        placement_decision_create_spec = cls()

        placement_decision_create_spec.additional_properties = d
        return placement_decision_create_spec

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
