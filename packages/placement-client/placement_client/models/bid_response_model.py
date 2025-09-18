from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from ..models.bid_status import BidStatus
from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.metric_value import MetricValue


T = TypeVar("T", bound="BidResponseModel")


@_attrs_define
class BidResponseModel:
    """
    Attributes:
        id (str):
        status (BidStatus):
        reason (Union[None, str]):
        msg (Union[None, str]):
        metrics (list['MetricValue']):
    """

    id: str
    status: BidStatus
    reason: Union[None, str]
    msg: Union[None, str]
    metrics: list["MetricValue"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status = self.status.value

        reason: Union[None, str]
        reason = self.reason

        msg: Union[None, str]
        msg = self.msg

        metrics = []
        for metrics_item_data in self.metrics:
            metrics_item = metrics_item_data.to_dict()
            metrics.append(metrics_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status": status,
                "reason": reason,
                "msg": msg,
                "metrics": metrics,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_value import MetricValue

        d = dict(src_dict)
        id = d.pop("id")

        status = BidStatus(d.pop("status"))

        def _parse_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reason = _parse_reason(d.pop("reason"))

        def _parse_msg(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        msg = _parse_msg(d.pop("msg"))

        metrics = []
        _metrics = d.pop("metrics")
        for metrics_item_data in _metrics:
            metrics_item = MetricValue.from_dict(metrics_item_data)

            metrics.append(metrics_item)

        bid_response_model = cls(
            id=id,
            status=status,
            reason=reason,
            msg=msg,
            metrics=metrics,
        )

        bid_response_model.additional_properties = d
        return bid_response_model

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
