from placement_controller.clients.k8s.client import KubeClient


class ObjectCache:
    client: KubeClient

    def __init__(self, client: KubeClient):
        self.client = client
