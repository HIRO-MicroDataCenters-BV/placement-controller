from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.namespaced_name_model import NamespacedNameModel


T = TypeVar("T", bound="TraceLogRowModel")


@_attrs_define
class TraceLogRowModel:
    """
    Attributes:
        timestamp (int):
        zone (str):
        name (NamespacedNameModel):
        msg (str):
        state (Union[None, Unset, str]):
    """

    timestamp: int
    zone: str
    name: "NamespacedNameModel"
    msg: str
    state: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp

        zone = self.zone

        name = self.name.to_dict()

        msg = self.msg

        state: Union[None, Unset, str]
        if isinstance(self.state, Unset):
            state = UNSET
        else:
            state = self.state

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
                "zone": zone,
                "name": name,
                "msg": msg,
            }
        )
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.namespaced_name_model import NamespacedNameModel

        d = dict(src_dict)
        timestamp = d.pop("timestamp")

        zone = d.pop("zone")

        name = NamespacedNameModel.from_dict(d.pop("name"))

        msg = d.pop("msg")

        def _parse_state(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        state = _parse_state(d.pop("state", UNSET))

        trace_log_row_model = cls(
            timestamp=timestamp,
            zone=zone,
            name=name,
            msg=msg,
            state=state,
        )

        trace_log_row_model.additional_properties = d
        return trace_log_row_model

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
