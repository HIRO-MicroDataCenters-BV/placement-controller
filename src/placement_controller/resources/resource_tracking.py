from typing import List

import asyncio

from placement_controller.clients.k8s.client import GroupVersionKind, KubeClient
from placement_controller.k8s.object_pool import ObjectPool
from placement_controller.resources.node import Node
from placement_controller.resources.pod import Pod
from placement_controller.resources.types import NodeInfo, ResourceTracking


class ResourceTrackingImpl(ResourceTracking):
    node_pool: ObjectPool[Node]
    node_task: asyncio.Task[None]
    pod_pool: ObjectPool[Pod]
    pod_task: asyncio.Task[None]
    is_terminated: asyncio.Event

    def __init__(self, client: KubeClient, is_terminated: asyncio.Event):
        self.node_pool = ObjectPool[Node](Node, client, GroupVersionKind("", "v1", "Node"), is_terminated)
        self.pod_pool = ObjectPool[Pod](Pod, client, GroupVersionKind("", "v1", "Pod"), is_terminated)

    def start(self) -> None:
        self.node_task = asyncio.create_task(self.node_pool.start())
        self.pod_task = asyncio.create_task(self.pod_pool.start())

    def list_nodes(self) -> List[NodeInfo]:
        nodes = {node.get_name(): NodeInfo.from_node(node) for node in self.node_pool.get_objects()}
        for pod in self.pod_pool.get_objects():
            node_name = pod.get_node_name()
            if node_name:
                node_info = nodes.get(node_name)
                if node_info:
                    node_info.add(pod)
        return list(nodes.values())
