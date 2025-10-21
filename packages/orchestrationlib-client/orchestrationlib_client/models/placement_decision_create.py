from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime

if TYPE_CHECKING:
    from ..models.placement_decision_id import PlacementDecisionID
    from ..models.placement_decision_field import PlacementDecisionField
    from ..models.placement_decision_create_spec import PlacementDecisionCreateSpec


T = TypeVar("T", bound="PlacementDecisionCreate")


@_attrs_define
class PlacementDecisionCreate:
    """Schema for creating a Placement Decision

    Attributes:
        id (PlacementDecisionID): Schema for Placement Decision ID
        spec (PlacementDecisionCreateSpec): Arbitrary spec JSON (free-form). Contains resources list. Example:
            {'resources': [{'id': {'name': 'name', 'namespace': 'ns'}, 'limits': {'cpu': '1', 'ephemeral-storage': '1g',
            'ram': '3'}, 'replicas': 2, 'requests': {'cpu': '1', 'nvidia/gpu': '1', 'ram': '3'}, 'type': 'pod'}, {'id':
            {'name': 'name', 'namespace': 'ns'}, 'replicas': 2, 'size': '1G', 'storageClass': 'default', 'type': 'pvc'}]}.
        decision (PlacementDecisionField): Schema for Placement Decision Field
        timestamp (Union[None, Unset, datetime.datetime]):
        trace (Union[None, Unset, str]):
    """

    id: "PlacementDecisionID"
    spec: "PlacementDecisionCreateSpec"
    decision: "PlacementDecisionField"
    timestamp: Union[None, Unset, datetime.datetime] = UNSET
    trace: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id.to_dict()

        spec = self.spec.to_dict()

        decision = self.decision.to_dict()

        timestamp: Union[None, Unset, str]
        if isinstance(self.timestamp, Unset):
            timestamp = UNSET
        elif isinstance(self.timestamp, datetime.datetime):
            timestamp = self.timestamp.isoformat()
        else:
            timestamp = self.timestamp

        trace: Union[None, Unset, str]
        if isinstance(self.trace, Unset):
            trace = UNSET
        else:
            trace = self.trace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "spec": spec,
                "decision": decision,
            }
        )
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if trace is not UNSET:
            field_dict["trace"] = trace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.placement_decision_id import PlacementDecisionID
        from ..models.placement_decision_field import PlacementDecisionField
        from ..models.placement_decision_create_spec import PlacementDecisionCreateSpec

        d = dict(src_dict)
        id = PlacementDecisionID.from_dict(d.pop("id"))

        spec = PlacementDecisionCreateSpec.from_dict(d.pop("spec"))

        decision = PlacementDecisionField.from_dict(d.pop("decision"))

        def _parse_timestamp(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                timestamp_type_0 = isoparse(data)

                return timestamp_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        timestamp = _parse_timestamp(d.pop("timestamp", UNSET))

        def _parse_trace(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        trace = _parse_trace(d.pop("trace", UNSET))

        placement_decision_create = cls(
            id=id,
            spec=spec,
            decision=decision,
            timestamp=timestamp,
            trace=trace,
        )

        placement_decision_create.additional_properties = d
        return placement_decision_create

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
