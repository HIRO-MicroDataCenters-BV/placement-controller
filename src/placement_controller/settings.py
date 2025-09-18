from typing import List

from pydantic_settings import BaseSettings

from placement_controller.clients.k8s.settings import K8SSettings


class PrometheusSettings(BaseSettings):
    endpoint_port: int = 8080


class ApiSettings(BaseSettings):
    port: int = 8000


class PlacementSettings(BaseSettings):
    namespace: str
    available_zones: List[str]
    current_zone: str


class Settings(BaseSettings):
    k8s: K8SSettings
    api: ApiSettings
    placement: PlacementSettings
    prometheus: PrometheusSettings
