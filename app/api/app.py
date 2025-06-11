from typing import List

from fastapi import Depends, FastAPI
from uvicorn import Config, Server

from app.core.applications import Application, Applications


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
    async def read_root():
        return {"message": "Hello from FastAPI"}

    @app.get("/applications/", response_model=List[Application])
    def list_applications(apps: Applications = Depends(lambda: get_applications(app))) -> List[Application]:
        return apps.list()

    return app


def get_applications(app: FastAPI) -> Applications:
    return app.state.applications  # type:ignore
