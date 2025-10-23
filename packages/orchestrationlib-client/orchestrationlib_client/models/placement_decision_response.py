from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast, Union
from uuid import UUID


T = TypeVar("T", bound="PlacementDecisionResponse")


@_attrs_define
class PlacementDecisionResponse:
    """Schema for responding with a Placement Decision

    Attributes:
        status (str):
        decision_id (Union[None, UUID, Unset]):
        summary (Union[None, Unset, str]):
        details (Union[None, Unset, str]):
    """

    status: str
    decision_id: Union[None, UUID, Unset] = UNSET
    summary: Union[None, Unset, str] = UNSET
    details: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        decision_id: Union[None, Unset, str]
        if isinstance(self.decision_id, Unset):
            decision_id = UNSET
        elif isinstance(self.decision_id, UUID):
            decision_id = str(self.decision_id)
        else:
            decision_id = self.decision_id

        summary: Union[None, Unset, str]
        if isinstance(self.summary, Unset):
            summary = UNSET
        else:
            summary = self.summary

        details: Union[None, Unset, str]
        if isinstance(self.details, Unset):
            details = UNSET
        else:
            details = self.details

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
            }
        )
        if decision_id is not UNSET:
            field_dict["decision_id"] = decision_id
        if summary is not UNSET:
            field_dict["summary"] = summary
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = d.pop("status")

        def _parse_decision_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                decision_id_type_0 = UUID(data)

                return decision_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        decision_id = _parse_decision_id(d.pop("decision_id", UNSET))

        def _parse_summary(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        summary = _parse_summary(d.pop("summary", UNSET))

        def _parse_details(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        details = _parse_details(d.pop("details", UNSET))

        placement_decision_response = cls(
            status=status,
            decision_id=decision_id,
            summary=summary,
            details=details,
        )

        placement_decision_response.additional_properties = d
        return placement_decision_response

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
