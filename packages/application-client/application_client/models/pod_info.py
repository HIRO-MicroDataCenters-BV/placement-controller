from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.log_info import LogInfo
    from ..models.pod_event import PodEvent


T = TypeVar("T", bound="PodInfo")


@_attrs_define
class PodInfo:
    """
    Attributes:
        name (str):
        status (str):
        restarts (int):
        events (list['PodEvent']):
        logs (list['LogInfo']):
    """

    name: str
    status: str
    restarts: int
    events: list["PodEvent"]
    logs: list["LogInfo"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        status = self.status

        restarts = self.restarts

        events = []
        for events_item_data in self.events:
            events_item = events_item_data.to_dict()
            events.append(events_item)

        logs = []
        for logs_item_data in self.logs:
            logs_item = logs_item_data.to_dict()
            logs.append(logs_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "status": status,
                "restarts": restarts,
                "events": events,
                "logs": logs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_info import LogInfo
        from ..models.pod_event import PodEvent

        d = dict(src_dict)
        name = d.pop("name")

        status = d.pop("status")

        restarts = d.pop("restarts")

        events = []
        _events = d.pop("events")
        for events_item_data in _events:
            events_item = PodEvent.from_dict(events_item_data)

            events.append(events_item)

        logs = []
        _logs = d.pop("logs")
        for logs_item_data in _logs:
            logs_item = LogInfo.from_dict(logs_item_data)

            logs.append(logs_item)

        pod_info = cls(
            name=name,
            status=status,
            restarts=restarts,
            events=events,
            logs=logs,
        )

        pod_info.additional_properties = d
        return pod_info

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
