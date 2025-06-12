from typing import List

from pydantic import BaseModel

from app.core.application import Application


class ApplicationModel(BaseModel):
    name: str
    namespace: str
    zones: List[str]

    @staticmethod
    def from_object(application: Application) -> "ApplicationModel":
        name = application.get_namespaced_name()
        zones = application.get_placement_zones()
        return ApplicationModel(name=name.name, namespace=name.namespace, zones=zones)
