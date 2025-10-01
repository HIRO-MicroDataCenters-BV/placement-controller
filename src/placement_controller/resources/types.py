from typing import List

from placement_controller.resources.node_info import NodeInfo


class ResourceTracking:

    async def start(self) -> None:
        raise NotImplementedError

    def list_nodes(self) -> List[NodeInfo]:
        raise NotImplementedError

    def is_subscription_active(self) -> bool:
        raise NotImplementedError
