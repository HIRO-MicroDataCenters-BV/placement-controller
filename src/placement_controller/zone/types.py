from placement_controller.clients.placement.types import PlacementClient


class ZoneApiFactory:
    def create(self, zone: str) -> PlacementClient:
        raise NotImplementedError()
