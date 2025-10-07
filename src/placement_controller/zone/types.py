from placement_client.client import Client


class ZoneApiFactory:
    def create(self, zone: str) -> Client:
        raise NotImplementedError()
