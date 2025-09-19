from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.workload_status import WorkloadStatus
    from ..models.pod_info import PodInfo


T = TypeVar("T", bound="ApplicationReport")


@_attrs_define
class ApplicationReport:
    """
    Attributes:
        pods (list['PodInfo']):
        workloads (list['WorkloadStatus']):
    """

    pods: list["PodInfo"]
    workloads: list["WorkloadStatus"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pods = []
        for pods_item_data in self.pods:
            pods_item = pods_item_data.to_dict()
            pods.append(pods_item)

        workloads = []
        for workloads_item_data in self.workloads:
            workloads_item = workloads_item_data.to_dict()
            workloads.append(workloads_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pods": pods,
                "workloads": workloads,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workload_status import WorkloadStatus
        from ..models.pod_info import PodInfo

        d = dict(src_dict)
        pods = []
        _pods = d.pop("pods")
        for pods_item_data in _pods:
            pods_item = PodInfo.from_dict(pods_item_data)

            pods.append(pods_item)

        workloads = []
        _workloads = d.pop("workloads")
        for workloads_item_data in _workloads:
            workloads_item = WorkloadStatus.from_dict(workloads_item_data)

            workloads.append(workloads_item)

        application_report = cls(
            pods=pods,
            workloads=workloads,
        )

        application_report.additional_properties = d
        return application_report

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
