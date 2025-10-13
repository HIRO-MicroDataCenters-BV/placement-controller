from typing import Any, Dict, List, Union

from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi
from uvicorn import Config, Server

from placement_controller.api.model import (
    ApplicationModel,
    ApplicationState,
    BidRequestModel,
    BidResponseModel,
    ErrorResponse,
)
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.applications import Applications
from placement_controller.resources.types import ResourceManagement


class PlacementFastAPI(FastAPI):
    def openapi(self) -> Dict[str, Any]:
        if self.openapi_schema:
            return self.openapi_schema
        openapi_schema = get_openapi(
            title="Placement Controller",
            version="0.0.0",
            description="Baseline Placement Controller for Decentralized Control Plance",
            contact={
                "name": "HIRO-MicroDataCenters",
                "email": "all-hiro@hiro-microdatacenters.nl",
            },
            license_info={
                "name": "MIT",
                "url": "https://github.com/HIRO-MicroDataCenters-BV" "/placement-controller/blob/main/LICENSE",
            },
            routes=self.routes,
        )
        self.openapi_schema = openapi_schema
        return self.openapi_schema


async def start_fastapi(port: int, applications: Applications, resource_management: ResourceManagement) -> None:
    app = create_app(applications, resource_management)
    config = Config(app=app, host="0.0.0.0", port=port, loop="asyncio")
    server = Server(config)

    # Start the server without blocking the current event loop
    await server.serve()


def create_app(applications: Applications, resource_management: ResourceManagement) -> PlacementFastAPI:
    app = create_api()

    app.state.applications = applications
    app.state.resource_management = resource_management

    return app


def create_api() -> PlacementFastAPI:
    app = PlacementFastAPI()

    @app.get(path="/", operation_id="status", description="Get Application Status")
    async def root():
        return {"application": "Placement Controller", "status": "OK"}

    @app.get(path="/applications/", response_model=List[ApplicationModel], operation_id="list_applications")
    async def list_applications(apps: Applications = Depends(lambda: get_applications(app))) -> List[ApplicationModel]:
        list_of_apps = await apps.list()
        return [ApplicationModel.from_object(app) for app in list_of_apps]

    @app.get(
        path="/applications/scheduling-state/",
        response_model=List[ApplicationState],
        operation_id="list_scheduling_state",
    )
    def list_scheduling_state(apps: Applications = Depends(lambda: get_applications(app))) -> List[ApplicationState]:
        return apps.list_scheduling_state()

    @app.put(
        "/applications/{namespace}/{name}/placements", response_model=ApplicationModel, operation_id="set_placements"
    )
    async def set_placements(
        namespace: str, name: str, zones: List[str], apps: Applications = Depends(lambda: get_applications(app))
    ) -> ApplicationModel:
        namespaced_name = NamespacedName(name=name, namespace=namespace)
        application = await apps.set_placement(namespaced_name, zones)
        return ApplicationModel.from_object(application)

    @app.put("/applications/{namespace}/{name}/owner", response_model=ApplicationModel, operation_id="set_owner")
    async def set_owner(
        namespace: str, name: str, owner: str, apps: Applications = Depends(lambda: get_applications(app))
    ) -> ApplicationModel:
        namespaced_name = NamespacedName(name=name, namespace=namespace)
        application = await apps.set_owner(namespaced_name, owner)
        return ApplicationModel.from_object(application)

    @app.put(
        "/bids/",
        response_model=BidResponseModel,
        operation_id="application_bid",
        responses={500: {"model": ErrorResponse}, 200: {"model": BidResponseModel}},
    )
    async def application_bid(
        bid: BidRequestModel, resource_management: ResourceManagement = Depends(lambda: get_resource_management(app))
    ) -> Union[BidResponseModel, ErrorResponse]:
        try:
            return resource_management.application_bid(bid)
        except Exception as e:
            return ErrorResponse(status=500, code="INTERNAL_ERROR", msg=str(e))

    return app


app = create_api()


def get_applications(app: FastAPI) -> Applications:
    return app.state.applications  # type:ignore


def get_resource_management(app: FastAPI) -> ResourceManagement:
    return app.state.resource_management  # type:ignore
