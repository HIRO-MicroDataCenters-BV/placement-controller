from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.resource_id import ResourceId


T = TypeVar("T", bound="PVCResources")


@_attrs_define
class PVCResources:
    """
    Attributes:
        id (ResourceId):
        replica (int):
        storage_class (str):
        size (Union[Unset, str]):
    """

    id: "ResourceId"
    replica: int
    storage_class: str
    size: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id.to_dict()

        replica = self.replica

        storage_class = self.storage_class

        size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "replica": replica,
                "storage-class": storage_class,
            }
        )
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_id import ResourceId

        d = dict(src_dict)
        id = ResourceId.from_dict(d.pop("id"))

        replica = d.pop("replica")

        storage_class = d.pop("storage-class")

        size = d.pop("size", UNSET)

        pvc_resources = cls(
            id=id,
            replica=replica,
            storage_class=storage_class,
            size=size,
        )

        pvc_resources.additional_properties = d
        return pvc_resources

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
