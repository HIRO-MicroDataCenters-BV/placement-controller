from typing import List

from dataclasses import dataclass


@dataclass
class NodeInfo:
    name: str


class ResourceTracking:

    async def start(self) -> None:
        raise NotImplementedError

    def list_nodes(self) -> List[NodeInfo]:
        raise NotImplementedError
