from typing import List

from pydantic import BaseModel

from placement.core.application import Application


class ApplicationModel(BaseModel):
    name: str
    namespace: str
    owner: str
    zones: List[str]

    @staticmethod
    def from_object(application: Application) -> "ApplicationModel":
        name = application.get_namespaced_name()
        zones = application.get_placement_zones()
        owner = application.get_owner_zone() or ""
        return ApplicationModel(name=name.name, namespace=name.namespace, zones=zones, owner=owner)
