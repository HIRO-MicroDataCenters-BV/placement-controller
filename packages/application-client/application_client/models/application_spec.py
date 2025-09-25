from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Union

if TYPE_CHECKING:
    from ..models.pod_resources import PodResources
    from ..models.resource_id import ResourceId
    from ..models.pvc_resources import PVCResources


T = TypeVar("T", bound="ApplicationSpec")


@_attrs_define
class ApplicationSpec:
    """
    Attributes:
        id (ResourceId):
        resources (list[Union['PVCResources', 'PodResources']]):
    """

    id: "ResourceId"
    resources: list[Union["PVCResources", "PodResources"]]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.pod_resources import PodResources

        id = self.id.to_dict()

        resources = []
        for resources_item_data in self.resources:
            resources_item: dict[str, Any]
            if isinstance(resources_item_data, PodResources):
                resources_item = resources_item_data.to_dict()
            else:
                resources_item = resources_item_data.to_dict()

            resources.append(resources_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "resources": resources,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pod_resources import PodResources
        from ..models.resource_id import ResourceId
        from ..models.pvc_resources import PVCResources

        d = dict(src_dict)
        id = ResourceId.from_dict(d.pop("id"))

        resources = []
        _resources = d.pop("resources")
        for resources_item_data in _resources:

            def _parse_resources_item(
                data: object,
            ) -> Union["PVCResources", "PodResources"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    resources_item_type_0 = PodResources.from_dict(data)

                    return resources_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                resources_item_type_1 = PVCResources.from_dict(data)

                return resources_item_type_1

            resources_item = _parse_resources_item(resources_item_data)

            resources.append(resources_item)

        application_spec = cls(
            id=id,
            resources=resources,
        )

        application_spec.additional_properties = d
        return application_spec

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
