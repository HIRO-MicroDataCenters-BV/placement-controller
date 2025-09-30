from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.pvc_resources_requests import PVCResourcesRequests
    from ..models.resource_id import ResourceId
    from ..models.pvc_resources_limits import PVCResourcesLimits


T = TypeVar("T", bound="PVCResources")


@_attrs_define
class PVCResources:
    """
    Attributes:
        id (ResourceId):
        replica (int):
        storage_class (str):
        requests (PVCResourcesRequests):
        limits (PVCResourcesLimits):
    """

    id: "ResourceId"
    replica: int
    storage_class: str
    requests: "PVCResourcesRequests"
    limits: "PVCResourcesLimits"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id.to_dict()

        replica = self.replica

        storage_class = self.storage_class

        requests = self.requests.to_dict()

        limits = self.limits.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "replica": replica,
                "storage-class": storage_class,
                "requests": requests,
                "limits": limits,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pvc_resources_requests import PVCResourcesRequests
        from ..models.resource_id import ResourceId
        from ..models.pvc_resources_limits import PVCResourcesLimits

        d = dict(src_dict)
        id = ResourceId.from_dict(d.pop("id"))

        replica = d.pop("replica")

        storage_class = d.pop("storage-class")

        requests = PVCResourcesRequests.from_dict(d.pop("requests"))

        limits = PVCResourcesLimits.from_dict(d.pop("limits"))

        pvc_resources = cls(
            id=id,
            replica=replica,
            storage_class=storage_class,
            requests=requests,
            limits=limits,
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
