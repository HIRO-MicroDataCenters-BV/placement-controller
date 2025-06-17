from typing import Any, Callable, Coroutine, Dict, Optional, Tuple, TypeVar, override

import asyncio
from dataclasses import dataclass

from kubernetes_asyncio import config
from kubernetes_asyncio.client import ApiClient, CustomObjectsApi
from kubernetes_asyncio.client.configuration import Configuration
from kubernetes_asyncio.dynamic import DynamicClient
from kubernetes_asyncio.watch import Watch
from loguru import logger

from app.clients.k8s.client import GroupVersionKind, KubeClient, NamespacedName, SubscriberId
from app.clients.k8s.event import EventType, KubeEvent
from app.clients.k8s.settings import K8SSettings
from app.core.async_queue import AsyncQueue

T = TypeVar("T")


@dataclass
class Subscription:
    queue: AsyncQueue[KubeEvent]
    task: asyncio.Task[Any]


class KubeClientImpl(KubeClient):
    settings: K8SSettings
    configuration: Optional[Configuration]
    subscriptions: Dict[SubscriberId, Subscription]
    subscriber_ids: SubscriberId
    loop: asyncio.AbstractEventLoop

    def __init__(self, settings: K8SSettings, loop: asyncio.AbstractEventLoop):
        self.settings = settings
        self.configuration = None
        self.subscriptions = {}
        self.subscriber_ids = 0
        self.loop = loop

    @override
    def watch(
        self,
        gvk: GroupVersionKind,
        namespace: Optional[str],
        version_since: int,
        is_terminated: asyncio.Event,
    ) -> Tuple[SubscriberId, AsyncQueue[KubeEvent]]:
        queue = AsyncQueue[KubeEvent]()

        async def watch_internal(api_client: ApiClient) -> None:
            while not is_terminated.is_set():
                try:
                    api = CustomObjectsApi(api_client)
                    w = Watch()
                    async for watch_event in w.stream(
                        lambda **kwargs: api.list_namespaced_custom_object(
                            group=gvk.group,
                            version=gvk.version,
                            namespace=namespace,
                            plural="anyapplications",
                            **kwargs,
                        ),
                        resource_version=str(version_since),
                        timeout_seconds=self.settings.timeout_seconds,
                    ):
                        try:
                            type = watch_event["type"]
                            object = watch_event["object"]
                            version = object["metadata"]["resourceVersion"]
                            event = KubeEvent(
                                event=EventType[type],
                                object=object,
                                version=version,
                            )
                            queue.put_nowait(event)
                        except Exception as e:
                            logger.error("error parsing error {exception}", exception=str(e))
                except Exception as e:
                    logger.error(f"watch exception {type(e)}: {e}")

        task = self.loop.create_task(self.execute(watch_internal, is_dynamic_client=False))
        subscription = Subscription(queue, task)

        self.subscriber_ids += 1
        subscriber_id = self.subscriber_ids

        self.subscriptions[subscriber_id] = subscription
        return subscriber_id, queue

    @override
    def stop_watch(self, subscriber_id: SubscriberId) -> None:
        self.subscriptions[subscriber_id].task.cancel()
        del self.subscriptions[subscriber_id]

    @override
    async def patch(self, gvk: GroupVersionKind, object: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        async def patch_internal(client: DynamicClient) -> Optional[Dict[str, Any]]:
            api = await client.resources.get(group=gvk.group, api_version=gvk.version, kind=gvk.kind)
            result = await api.patch(body=object, content_type="application/merge-patch+json")
            result_dict: Dict[str, Any] = result.to_dict()
            if result_dict.get("status") == "Failure" and result_dict.get("code") == 404:
                return None
            return result_dict

        return await self.execute(patch_internal)

    @override
    async def patch_status(
        self, gvk: GroupVersionKind, name: NamespacedName, status: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        async def patch_status_internal(client: DynamicClient) -> Optional[Dict[str, Any]]:
            api = await client.resources.get(group=gvk.group, api_version=gvk.version, kind=gvk.kind)
            result = await api.status.patch(
                name=name.name, namespace=name.namespace, body=status, content_type="application/merge-patch+json"
            )
            result_dict: Dict[str, Any] = result.to_dict()
            if result_dict.get("status") == "Failure" and result_dict.get("code") == 404:
                return None
            return result_dict

        return await self.execute(patch_status_internal)

    @override
    async def get(self, gvk: GroupVersionKind, name: NamespacedName) -> Optional[Dict[str, Any]]:
        async def get_internal(client: DynamicClient) -> Optional[Dict[str, Any]]:
            api = await client.resources.get(group=gvk.group, api_version=gvk.version, kind=gvk.kind)
            result = await api.get(name=name.name, namespace=name.namespace)
            result_dict: Dict[str, Any] = result.to_dict()
            if result_dict.get("status") == "Failure" and result_dict.get("code") == 404:
                return None
            return result_dict

        return await self.execute(get_internal)

    @override
    async def delete(self, gvk: GroupVersionKind, name: NamespacedName) -> Optional[Dict[str, Any]]:
        async def delete_internal(client: DynamicClient) -> Optional[Dict[str, Any]]:
            api = await client.resources.get(group=gvk.group, api_version=gvk.version, kind=gvk.kind)
            result = await api.delete(name=name.name, namespace=name.namespace)
            result_dict: Dict[str, Any] = result.to_dict()
            if result_dict.get("status") == "Failure" and result_dict.get("code") == 404:
                return None
            return result_dict

        return await self.execute(delete_internal)

    async def execute(
        self, func: Callable[[DynamicClient | ApiClient], Coroutine[Any, Any, T]], is_dynamic_client: bool = True
    ) -> T:
        await self.init_configuration()

        async with ApiClient(configuration=self.configuration) as client_api:
            if is_dynamic_client:
                async with DynamicClient(client_api) as dynamic_api:
                    return await func(dynamic_api)
            else:
                return await func(client_api)

    async def init_configuration(self) -> None:
        if not self.configuration:
            self.configuration = Configuration()
            if self.settings.incluster:
                config.load_incluster_config(client_configuration=self.configuration)
            else:
                await config.load_kube_config(client_configuration=self.configuration, context=self.settings.context)
