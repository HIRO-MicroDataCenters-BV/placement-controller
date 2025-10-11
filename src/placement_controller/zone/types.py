from placement_client.client import Client


class ZoneApiFactory:
    def create(self, zone: str) -> Client:
        raise NotImplementedError()

    def is_local(self, zone: str) -> bool:
        raise NotImplementedError()
