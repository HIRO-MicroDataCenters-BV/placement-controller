from fastapi import Depends, FastAPI, Request, Response

from placement_controller.jobs.fake_server import FakeServer


class FakeOrchestrationlibServer(FakeServer):

    status: int

    def __init__(self, host: str):
        app = FastAPI()

        self.status = 500

        @app.get("/placement_decisions/", response_model=None)
        def save_decision(
            request: Request,
            server: FakeOrchestrationlibServer = Depends(lambda: self),
        ) -> Response:
            return Response(content="OK", status_code=server.status)

        super().__init__(host, app)
