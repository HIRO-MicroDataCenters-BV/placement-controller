from typing import Union

import json

from application_client import models
from fastapi import Depends, FastAPI, Response

from placement_controller.jobs.fake_server import FakeServer


class FakeApplicationController(FakeServer):

    mocked_spec: Union[models.ApplicationSpec, models.ErrorResponse]
    status: int

    def __init__(self, host: str, port: int):
        self.base_url = f"http://{host}:{port}"

        app = FastAPI()
        self.mocked_spec = models.ErrorResponse(status=500, code="INTERNAL_ERROR", message="mocked spec is not set")
        self.status = 500

        @app.get("/applications/{namespace}/{name}/specification", response_model=None)
        def get_application_spec(
            namespace: str,
            name: str,
            server: FakeApplicationController = Depends(lambda: self),
        ) -> Response:
            return Response(content=json.dumps(server.mocked_spec.to_dict()), status_code=server.status)

        super().__init__(host, port, app)

    def mock_response(self, spec: Union[models.ApplicationSpec, models.ErrorResponse]) -> None:
        self.mocked_spec = spec
        self.status = 200
