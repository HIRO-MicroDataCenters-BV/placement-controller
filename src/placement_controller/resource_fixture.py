from typing import Any, Dict


class ResourceTestFixture:

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
