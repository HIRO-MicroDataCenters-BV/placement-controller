from pydantic_settings import BaseSettings

from app.clients.k8s.settings import K8SSettings


class PrometheusSettings(BaseSettings):
    endpoint_port: int = 8080


class Settings(BaseSettings):
    k8s: K8SSettings
    prometheus: PrometheusSettings
