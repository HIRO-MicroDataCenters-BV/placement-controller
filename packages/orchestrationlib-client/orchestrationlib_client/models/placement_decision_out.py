from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime

if TYPE_CHECKING:
    from ..models.placement_decision_out_spec import PlacementDecisionOutSpec


T = TypeVar("T", bound="PlacementDecisionOut")


@_attrs_define
class PlacementDecisionOut:
    """Schema for outputting a Placement Decision

    Attributes:
        decision_id (UUID):
        name (str):
        namespace (str):
        spec (PlacementDecisionOutSpec):
        decision_placement_lst (list[str]):
        decision_reason (str):
        timestamp (datetime.datetime):
        trace (Union[None, Unset, str]):
    """

    decision_id: UUID
    name: str
    namespace: str
    spec: "PlacementDecisionOutSpec"
    decision_placement_lst: list[str]
    decision_reason: str
    timestamp: datetime.datetime
    trace: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        decision_id = str(self.decision_id)

        name = self.name

        namespace = self.namespace

        spec = self.spec.to_dict()

        decision_placement_lst = self.decision_placement_lst

        decision_reason = self.decision_reason

        timestamp = self.timestamp.isoformat()

        trace: Union[None, Unset, str]
        if isinstance(self.trace, Unset):
            trace = UNSET
        else:
            trace = self.trace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "decision_id": decision_id,
                "name": name,
                "namespace": namespace,
                "spec": spec,
                "decision_placement_lst": decision_placement_lst,
                "decision_reason": decision_reason,
                "timestamp": timestamp,
            }
        )
        if trace is not UNSET:
            field_dict["trace"] = trace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.placement_decision_out_spec import PlacementDecisionOutSpec

        d = dict(src_dict)
        decision_id = UUID(d.pop("decision_id"))

        name = d.pop("name")

        namespace = d.pop("namespace")

        spec = PlacementDecisionOutSpec.from_dict(d.pop("spec"))

        decision_placement_lst = cast(list[str], d.pop("decision_placement_lst"))

        decision_reason = d.pop("decision_reason")

        timestamp = isoparse(d.pop("timestamp"))

        def _parse_trace(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        trace = _parse_trace(d.pop("trace", UNSET))

        placement_decision_out = cls(
            decision_id=decision_id,
            name=name,
            namespace=namespace,
            spec=spec,
            decision_placement_lst=decision_placement_lst,
            decision_reason=decision_reason,
            timestamp=timestamp,
            trace=trace,
        )

        placement_decision_out.additional_properties = d
        return placement_decision_out

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
