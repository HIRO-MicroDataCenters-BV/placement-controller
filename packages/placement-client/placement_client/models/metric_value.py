from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from ..models.metric import Metric
from ..models.metric_unit import MetricUnit


T = TypeVar("T", bound="MetricValue")


@_attrs_define
class MetricValue:
    """
    Attributes:
        id (Metric):
        value (str):
        unit (MetricUnit):
    """

    id: Metric
    value: str
    unit: MetricUnit
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id.value

        value = self.value

        unit = self.unit.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "value": value,
                "unit": unit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = Metric(d.pop("id"))

        value = d.pop("value")

        unit = MetricUnit(d.pop("unit"))

        metric_value = cls(
            id=id,
            value=value,
            unit=unit,
        )

        metric_value.additional_properties = d
        return metric_value

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
