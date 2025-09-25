from typing import List

from placement_controller.clients.k8s.client import KubeClient
from placement_controller.resources.types import NodeInfo, ResourceTracking


class ResourceTrackingImpl(ResourceTracking):
    client: KubeClient

    def __init__(self, client: KubeClient):
        self.client = client

    async def start(self) -> None:
        pass

    def list_nodes(self) -> List[NodeInfo]:
        return []
