from typing import List

import datetime
import json
from datetime import timezone

from loguru import logger
from orchestrationlib_client.api.placement_decisions import save_decision_placement_decisions_post
from orchestrationlib_client.client import Client
from orchestrationlib_client.models.placement_decision_create import PlacementDecisionCreate
from orchestrationlib_client.models.placement_decision_create_spec import PlacementDecisionCreateSpec
from orchestrationlib_client.models.placement_decision_field import PlacementDecisionField
from orchestrationlib_client.models.placement_decision_id import PlacementDecisionID

from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.store.types import DecisionStore


class DecisionStoreImpl(DecisionStore):
    client: Client

    def __init__(self, client: Client):
        self.client = client

    async def save(
        self,
        name: NamespacedName,
        spec: str,
        placement: List[str],
        reason: str,
        trace: str,
        timestamp: int,
    ) -> None:
        decision_id = PlacementDecisionID(name=name.name, namespace=name.namespace)
        spec_dict = json.loads(spec)
        create_spec = PlacementDecisionCreateSpec.from_dict(spec_dict)
        ts = datetime.datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        request = PlacementDecisionCreate(
            id=decision_id,
            spec=create_spec,
            decision=PlacementDecisionField(placement=placement, reason=reason),
            timestamp=ts,
            trace=trace,
        )
        response = await save_decision_placement_decisions_post.asyncio(client=self.client, body=request)
        if response is None:
            raise Exception("Empty response received while saving decision.")
        logger.info(f"{name}: Save decision response: {response}")
