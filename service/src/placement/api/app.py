from typing import List

from fastapi import Depends, FastAPI
from uvicorn import Config, Server

from app.api.model import ApplicationModel
from app.clients.k8s.client import NamespacedName
from app.core.applications import Applications


async def start_fastapi(port: int, applications: Applications) -> None:
    app = create_app(applications)
    config = Config(app=app, host="0.0.0.0", port=port, loop="asyncio")
    server = Server(config)

    # Start the server without blocking the current event loop
    await server.serve()


def create_app(applications: Applications) -> FastAPI:
    app = FastAPI()
    app.state.applications = applications

    @app.get("/")
    async def root():
        return {"application": "Placement Controller", "status": "OK"}

    @app.get("/applications/", response_model=List[ApplicationModel])
    def list_applications(apps: Applications = Depends(lambda: get_applications(app))) -> List[ApplicationModel]:
        return [ApplicationModel.from_object(app) for app in apps.list()]

    @app.put("/applications/{namespace}/{name}/placements", response_model=ApplicationModel)
    async def set_placements(
        namespace: str, name: str, zones: List[str], apps: Applications = Depends(lambda: get_applications(app))
    ) -> ApplicationModel:
        namespaced_name = NamespacedName(name=name, namespace=namespace)
        application = await apps.set_placement(namespaced_name, zones)
        return ApplicationModel.from_object(application)

    @app.put("/applications/{namespace}/{name}/owner", response_model=ApplicationModel)
    async def set_owner(
        namespace: str, name: str, owner: str, apps: Applications = Depends(lambda: get_applications(app))
    ) -> ApplicationModel:
        namespaced_name = NamespacedName(name=name, namespace=namespace)
        application = await apps.set_owner(namespaced_name, owner)
        return ApplicationModel.from_object(application)

    return app


def get_applications(app: FastAPI) -> Applications:
    return app.state.applications  # type:ignore
