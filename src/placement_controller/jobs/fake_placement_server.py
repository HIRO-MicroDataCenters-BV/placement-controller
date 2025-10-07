from typing import Union

import json

from fastapi import Depends, FastAPI, Response
from placement_client import models

from placement_controller.jobs.fake_server import FakeServer


class FakePlacementController(FakeServer):

    mocked_bid_response: Union[models.BidResponseModel, models.ErrorResponse]
    status: int

    def __init__(self, host: str, port: int):
        self.base_url = f"http://{host}:{port}"

        app = FastAPI()
        self.mocked_spec = models.ErrorResponse(status=500, code="INTERNAL_ERROR", msg="mocked bid response is not set")
        self.status = 500

        @app.put("/bids/", response_model=None)
        def application_bid(
            bid: models.BidRequestModel,
            server: FakePlacementController = Depends(lambda: self),
        ) -> Response:
            return Response(content=json.dumps(server.mocked_bid_response.to_dict()), status_code=server.status)

        super().__init__(host, port, app)

    def mock_response(self, spec: Union[models.BidResponseModel, models.ErrorResponse]) -> None:
        self.mocked_bid_response = spec
        self.status = 200
