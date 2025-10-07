from typing import Dict

from placement_client.client import Client

from placement_controller.zone.types import ZoneApiFactory

ZoneId = str
ZoneDomain = str
BaseUrl = str


class ZoneApiFactoryImpl(ZoneApiFactory):
    zone_to_domain: Dict[ZoneId, ZoneDomain]
    static_zones: Dict[ZoneId, BaseUrl]

    def __init__(self):
        self.zone_to_domain = dict()
        self.static_zones = dict()

    def add_static_zone(self, zone: ZoneId, url: BaseUrl) -> None:
        self.static_zones[zone] = url

    def create(self, zone: ZoneId) -> Client:
        base_url = self.static_zones.get(zone)
        if base_url:
            return Client(base_url=base_url)
        else:
            raise NotImplementedError("static zone is not configured, zone-to-domain mapping is not implemented")
