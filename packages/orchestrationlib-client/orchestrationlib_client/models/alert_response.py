from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.alert_type import AlertType
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime


T = TypeVar("T", bound="AlertResponse")


@_attrs_define
class AlertResponse:
    """Pydantic model for alert response.

    Attributes:
        id (int): Unique identifier for the alert
        alert_type (AlertType): Enum for alert types.
        alert_model (str): Model used for the alert
        alert_description (str): Description of the alert
        pod_id (Union[None, UUID]): ID of the pod
        node_id (Union[None, UUID]): ID of the node
        created_at (datetime.datetime): Timestamp when the alert was created
        source_ip (Union[None, Unset, str]): Source IP address
        source_port (Union[None, Unset, int]): Source port number
        destination_ip (Union[None, Unset, str]): Destination IP address
        destination_port (Union[None, Unset, int]): Destination port number
        protocol (Union[None, Unset, str]): Network protocol used
    """

    id: int
    alert_type: AlertType
    alert_model: str
    alert_description: str
    pod_id: Union[None, UUID]
    node_id: Union[None, UUID]
    created_at: datetime.datetime
    source_ip: Union[None, Unset, str] = UNSET
    source_port: Union[None, Unset, int] = UNSET
    destination_ip: Union[None, Unset, str] = UNSET
    destination_port: Union[None, Unset, int] = UNSET
    protocol: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        alert_type = self.alert_type.value

        alert_model = self.alert_model

        alert_description = self.alert_description

        pod_id: Union[None, str]
        if isinstance(self.pod_id, UUID):
            pod_id = str(self.pod_id)
        else:
            pod_id = self.pod_id

        node_id: Union[None, str]
        if isinstance(self.node_id, UUID):
            node_id = str(self.node_id)
        else:
            node_id = self.node_id

        created_at = self.created_at.isoformat()

        source_ip: Union[None, Unset, str]
        if isinstance(self.source_ip, Unset):
            source_ip = UNSET
        else:
            source_ip = self.source_ip

        source_port: Union[None, Unset, int]
        if isinstance(self.source_port, Unset):
            source_port = UNSET
        else:
            source_port = self.source_port

        destination_ip: Union[None, Unset, str]
        if isinstance(self.destination_ip, Unset):
            destination_ip = UNSET
        else:
            destination_ip = self.destination_ip

        destination_port: Union[None, Unset, int]
        if isinstance(self.destination_port, Unset):
            destination_port = UNSET
        else:
            destination_port = self.destination_port

        protocol: Union[None, Unset, str]
        if isinstance(self.protocol, Unset):
            protocol = UNSET
        else:
            protocol = self.protocol

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "alert_type": alert_type,
                "alert_model": alert_model,
                "alert_description": alert_description,
                "pod_id": pod_id,
                "node_id": node_id,
                "created_at": created_at,
            }
        )
        if source_ip is not UNSET:
            field_dict["source_ip"] = source_ip
        if source_port is not UNSET:
            field_dict["source_port"] = source_port
        if destination_ip is not UNSET:
            field_dict["destination_ip"] = destination_ip
        if destination_port is not UNSET:
            field_dict["destination_port"] = destination_port
        if protocol is not UNSET:
            field_dict["protocol"] = protocol

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        alert_type = AlertType(d.pop("alert_type"))

        alert_model = d.pop("alert_model")

        alert_description = d.pop("alert_description")

        def _parse_pod_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pod_id_type_0 = UUID(data)

                return pod_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        pod_id = _parse_pod_id(d.pop("pod_id"))

        def _parse_node_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                node_id_type_0 = UUID(data)

                return node_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        node_id = _parse_node_id(d.pop("node_id"))

        created_at = isoparse(d.pop("created_at"))

        def _parse_source_ip(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        source_ip = _parse_source_ip(d.pop("source_ip", UNSET))

        def _parse_source_port(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        source_port = _parse_source_port(d.pop("source_port", UNSET))

        def _parse_destination_ip(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        destination_ip = _parse_destination_ip(d.pop("destination_ip", UNSET))

        def _parse_destination_port(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        destination_port = _parse_destination_port(d.pop("destination_port", UNSET))

        def _parse_protocol(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        protocol = _parse_protocol(d.pop("protocol", UNSET))

        alert_response = cls(
            id=id,
            alert_type=alert_type,
            alert_model=alert_model,
            alert_description=alert_description,
            pod_id=pod_id,
            node_id=node_id,
            created_at=created_at,
            source_ip=source_ip,
            source_port=source_port,
            destination_ip=destination_ip,
            destination_port=destination_port,
            protocol=protocol,
        )

        alert_response.additional_properties = d
        return alert_response

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
