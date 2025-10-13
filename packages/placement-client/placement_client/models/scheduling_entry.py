from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast
from typing import Union


T = TypeVar("T", bound="SchedulingEntry")


@_attrs_define
class SchedulingEntry:
    """
    Attributes:
        seq_nr (int):
        state (str):
        msg (Union[None, str]):
        running_jobs (list[str]):
    """

    seq_nr: int
    state: str
    msg: Union[None, str]
    running_jobs: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        seq_nr = self.seq_nr

        state = self.state

        msg: Union[None, str]
        msg = self.msg

        running_jobs = self.running_jobs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "seq_nr": seq_nr,
                "state": state,
                "msg": msg,
                "running_jobs": running_jobs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        seq_nr = d.pop("seq_nr")

        state = d.pop("state")

        def _parse_msg(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        msg = _parse_msg(d.pop("msg"))

        running_jobs = cast(list[str], d.pop("running_jobs"))

        scheduling_entry = cls(
            seq_nr=seq_nr,
            state=state,
            msg=msg,
            running_jobs=running_jobs,
        )

        scheduling_entry.additional_properties = d
        return scheduling_entry

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
