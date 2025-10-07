from typing import Union

import json

from fastapi import Depends, FastAPI, Request, Response
from placement_client import models

from placement_controller.jobs.fake_server import FakeServer


class FakePlacementController(FakeServer):

    mocked_bid_response: Union[models.BidResponseModel, models.ErrorResponse]
    status: int

    def __init__(self, host: str):
        app = FastAPI()
        self.mocked_spec = models.ErrorResponse(status=500, code="INTERNAL_ERROR", msg="mocked bid response is not set")
        self.status = 500

        @app.put("/bids/", response_model=None)
        def application_bid(
            body: Request,
            server: FakePlacementController = Depends(lambda: self),
        ) -> Response:
            return Response(content=json.dumps(server.mocked_bid_response.to_dict()), status_code=server.status)

        super().__init__(host, app)

    def mock_response(self, response: Union[models.BidResponseModel, models.ErrorResponse]) -> None:
        self.mocked_bid_response = response
        self.status = 200
