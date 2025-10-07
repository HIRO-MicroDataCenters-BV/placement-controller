import asyncio
import threading

import httpx
import uvicorn
from fastapi import FastAPI, Response


class FakeServer:
    host: str
    port: int
    server_thread: threading.Thread
    server: uvicorn.Server

    app: FastAPI

    def __init__(self, host: str, port: int, app: FastAPI):
        self.port = port
        self.host = host
        self.base_url = f"http://{self.host}:{self.port}"
        self.app = app

        @self.app.get("/", response_model=None)
        def root() -> Response:
            return Response(content="OK", status_code=200, media_type="text/plain")

        config = uvicorn.Config(self.app, host=self.host, port=self.port, log_level="error")
        self.server = uvicorn.Server(config)
        self.server_thread = threading.Thread(target=lambda: asyncio.run(self.server.serve()), daemon=True)

    def start(self) -> None:
        self.server_thread.start()

    def is_available(self) -> bool:
        response = httpx.get(url=f"{self.base_url}/")
        return response.status_code == 200

    def stop(self) -> None:
        self.server.should_exit = True

    def get_base_url(self) -> str:
        return self.base_url

    def run(self):
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="error")
