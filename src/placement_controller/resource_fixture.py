from typing import Any, Dict, List

from application_client.models.pod_resources import PodResources
from application_client.models.pod_resources_limits import PodResourcesLimits
from application_client.models.pod_resources_requests import PodResourcesRequests
from application_client.models.resource_id import ResourceId

from placement_controller.clients.k8s.client import GroupVersionKind


class ResourceTestFixture:
    pod_gvk: GroupVersionKind = GroupVersionKind("", "v1", "Pod")
    node_gvk: GroupVersionKind = GroupVersionKind("", "v1", "Node")

    GIGA: int = 1024 * 1024 * 1024

    def simple_pod(self) -> Dict[str, Any]:
        return {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": "nginx",
                "namespace": "test",
            },
            "spec": {
                "containers": [
                    {
                        "name": "nginx",
                        "image": "nginx:1.14.2",
                        "ports": [{"containerPort": 80}],
                        "resources": {
                            "requests": {
                                "cpu": "100m",
                                "memory": "100Mi",
                            },
                            "limits": {
                                "cpu": "200m",
                                "memory": "200Mi",
                            },
                        },
                    }
                ],
            },
        }

    def simple_node(self) -> Dict[str, Any]:
        return {
            "apiVersion": "v1",
            "kind": "Node",
            "metadata": {
                "name": "node1",
            },
            "spec": {"podCIDR": "192.168.1.0/24"},
            "status": {
                "allocatable": {
                    "cpu": "10",
                    "memory": "8025424Ki",
                    "ephemeral-storage": "131787236Ki",
                },
            },
        }

    def make_node(self, name: str, cpu: int, memory: int, ephemeral_storage: int, gpu: int) -> Dict[str, Any]:
        allocatable = {
            "cpu": str(cpu),
            "memory": str(memory),
            "ephemeral-storage": str(ephemeral_storage),
        }
        if gpu > 0:
            allocatable["nvidia.com/gpu"] = str(gpu)
        return {
            "apiVersion": "v1",
            "kind": "Node",
            "metadata": {
                "name": name,
            },
            "spec": {"podCIDR": "192.168.1.0/24"},
            "status": {
                "allocatable": allocatable,
            },
        }

    def make_pod(self, name: str, requests: Dict[str, Any], limits: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": name,
                "namespace": "test",
            },
            "spec": {
                "containers": [
                    {
                        "name": "nginx",
                        "image": "nginx:1.14.2",
                        "ports": [{"containerPort": 80}],
                        "resources": {
                            "requests": requests,
                            "limits": limits,
                        },
                    }
                ],
            },
        }

    def make_pod_spec(self, name: str, replica: int, requests: Dict[str, Any], limits: Dict[str, Any]) -> PodResources:
        return PodResources(
            id=ResourceId(name=name, namespace="test"),
            replica=replica,
            requests=PodResourcesRequests.from_dict(requests),
            limits=PodResourcesLimits.from_dict(limits),
        )

    def mesh_peer(self, zone_id: str) -> Dict[str, Any]:
        return {
            "apiVersion": "dcp.hiro.io/v1",
            "kind": "MeshPeer",
            "metadata": {
                "name": zone_id,
                "namespace": "test",
            },
            "spec": {
                "identity": {
                    "endpoints": [],
                    "publicKey": "hex",
                }
            },
            "status": {
                "conditions": [
                    {
                        "lastTransitionTime": "2025-10-01T12:43:49Z",
                        "status": "True",
                        "type": "Ready",
                    }
                ],
                "instance": {
                    "start_time": "2025-10-01T12:43:49Z",
                    "start_timestamp": 1759322629932,
                    "zone": zone_id,
                },
                "status": "Ready",
                "updateTime": "2025-10-01T12:43:49Z",
            },
        }

    def make_anyapp(self, name: str, zones: str) -> Dict[str, Any]:
        return {
            "apiVersion": "dcp.hiro.io/v1",
            "kind": "AnyApplication",
            "metadata": {
                "name": name,
                "namespace": "test",
            },
            "spec": {
                "application": {
                    "helm": {
                        "chart": "nginx-ingress",
                        "namespace": "nginx",
                        "repository": "https://helm.nginx.com/stable",
                        "version": "2.0.1",
                    }
                },
                "placement-strategy": {"strategy": "Local"},
                "recover-strategy": {"max-retries": 3, "tolerance": 1},
                "zones": zones,
            },
        }

    def make_anyapp_status(self, state: str, owner: str, placements: List[str]) -> Dict[str, Any]:
        return {
            "status": {
                "state": state,
                "owner": owner,
                "placements": [{"node-affinity": None, "zone": placement} for placement in placements],
                "conditions": [
                    {
                        "lastTransitionTime": "2025-06-04T09:40:41Z",
                        "status": "status",
                        "type": "conditionType",
                        "zoneId": "zone1",
                        "zoneVersion": "1",
                    }
                ],
            }
        }
