from unittest import TestCase

from application_client.models.application_spec import ApplicationSpec
from application_client.models.resource_id import ResourceId

from placement_controller.resources.placement import GreedyPlacement


class PlacementTest(TestCase):
    placement: GreedyPlacement

    def setUp(self) -> None:
        self.placement = GreedyPlacement(
            nodes=[],
            spec=ApplicationSpec(id=ResourceId(name="test", namespace="test"), resources=[]),
            bidCriteria=[],
            metrics=[],
        )

    def test_placement(self):
        self.placement.try_bind()
