from typing import Dict

from placement_client.client import Client

from placement_controller.clients.placement.remote import RemotePlacementClient
from placement_controller.clients.placement.types import PlacementClient
from placement_controller.settings import PlacementSettings
from placement_controller.zone.types import ZoneApiFactory

ZoneId = str
ZoneDomain = str
BaseUrl = str


class ZoneApiFactoryImpl(ZoneApiFactory):
    local_client: PlacementClient
    zone_to_domain: Dict[ZoneId, ZoneDomain]
    static_zones: Dict[ZoneId, BaseUrl]
    local_zone: str

    def __init__(self, config: PlacementSettings, local_client: PlacementClient):
        self.local_client = local_client
        self.local_zone = config.current_zone
        self.zone_to_domain = dict()
        self.static_zones = config.static_controller_endpoints or dict()

    def set_local_client(self, local_client: PlacementClient) -> None:
        self.local_client = local_client

    def add_static_zone(self, zone: ZoneId, url: BaseUrl) -> None:
        self.static_zones[zone] = url

    def create(self, zone: ZoneId) -> PlacementClient:
        if self.local_zone == zone:
            return self.local_client
        else:
            base_url = self.static_zones.get(zone)
            if base_url:
                return RemotePlacementClient(Client(base_url=base_url))
            else:
                raise NotImplementedError(
                    f"static zone '{zone}' is not configured, zone-to-domain mapping is not implemented"
                )
