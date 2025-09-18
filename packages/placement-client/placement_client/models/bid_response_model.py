from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

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
        metrics (list['MetricValue']):
        reason (Union[None, Unset, str]):
        msg (Union[None, Unset, str]):
    """

    id: str
    status: BidStatus
    metrics: list["MetricValue"]
    reason: Union[None, Unset, str] = UNSET
    msg: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status = self.status.value

        metrics = []
        for metrics_item_data in self.metrics:
            metrics_item = metrics_item_data.to_dict()
            metrics.append(metrics_item)

        reason: Union[None, Unset, str]
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        msg: Union[None, Unset, str]
        if isinstance(self.msg, Unset):
            msg = UNSET
        else:
            msg = self.msg

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status": status,
                "metrics": metrics,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason
        if msg is not UNSET:
            field_dict["msg"] = msg

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_value import MetricValue

        d = dict(src_dict)
        id = d.pop("id")

        status = BidStatus(d.pop("status"))

        metrics = []
        _metrics = d.pop("metrics")
        for metrics_item_data in _metrics:
            metrics_item = MetricValue.from_dict(metrics_item_data)

            metrics.append(metrics_item)

        def _parse_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        reason = _parse_reason(d.pop("reason", UNSET))

        def _parse_msg(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        msg = _parse_msg(d.pop("msg", UNSET))

        bid_response_model = cls(
            id=id,
            status=status,
            metrics=metrics,
            reason=reason,
            msg=msg,
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
