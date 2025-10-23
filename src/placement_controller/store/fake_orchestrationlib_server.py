from typing import List

import json
import uuid

from fastapi import Depends, FastAPI, Request, Response
from orchestrationlib_client.models.placement_decision_create import PlacementDecisionCreate
from orchestrationlib_client.models.placement_decision_response import PlacementDecisionResponse

from placement_controller.jobs.fake_server import FakeServer


class FakeOrchestrationlibServer(FakeServer):

    status: int
    requests: List[PlacementDecisionCreate]
    response: PlacementDecisionResponse

    def __init__(self, host: str):
        app = FastAPI()

        self.status = 200
        self.requests = []
        self.response = PlacementDecisionResponse(
            status="OK",
            decision_id=uuid.uuid4(),
            summary="saved",
            details=None,
        )

        @app.post("/placement_decisions/", response_model=None)
        async def save(
            request: Request,
            server: FakeOrchestrationlibServer = Depends(lambda: self),
        ) -> Response:
            body = await request.body()
            request_body = PlacementDecisionCreate.from_dict(json.loads(body))
            server.requests.append(request_body)

            response_body = json.dumps(server.response.to_dict())
            return Response(content=response_body, status_code=server.status, media_type="application/json")

        super().__init__(host, app)

    def get_save_requests(self) -> List[PlacementDecisionCreate]:
        return self.requests
