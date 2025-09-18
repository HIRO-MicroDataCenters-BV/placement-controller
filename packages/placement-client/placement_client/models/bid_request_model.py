from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from ..models.bid_criteria import BidCriteria
from ..models.metric import Metric


T = TypeVar("T", bound="BidRequestModel")


@_attrs_define
class BidRequestModel:
    """
    Attributes:
        id (str):
        spec (str):
        bid_criteria (list[BidCriteria]):
        metrics (list[Metric]):
    """

    id: str
    spec: str
    bid_criteria: list[BidCriteria]
    metrics: list[Metric]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        spec = self.spec

        bid_criteria = []
        for bid_criteria_item_data in self.bid_criteria:
            bid_criteria_item = bid_criteria_item_data.value
            bid_criteria.append(bid_criteria_item)

        metrics = []
        for metrics_item_data in self.metrics:
            metrics_item = metrics_item_data.value
            metrics.append(metrics_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "spec": spec,
                "bidCriteria": bid_criteria,
                "metrics": metrics,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        spec = d.pop("spec")

        bid_criteria = []
        _bid_criteria = d.pop("bidCriteria")
        for bid_criteria_item_data in _bid_criteria:
            bid_criteria_item = BidCriteria(bid_criteria_item_data)

            bid_criteria.append(bid_criteria_item)

        metrics = []
        _metrics = d.pop("metrics")
        for metrics_item_data in _metrics:
            metrics_item = Metric(metrics_item_data)

            metrics.append(metrics_item)

        bid_request_model = cls(
            id=id,
            spec=spec,
            bid_criteria=bid_criteria,
            metrics=metrics,
        )

        bid_request_model.additional_properties = d
        return bid_request_model

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
