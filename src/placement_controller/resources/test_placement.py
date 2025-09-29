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
            bid_criteria=[],
        )

    def test_placement_empty(self):
        result = self.placement.try_place()

        self.assertTrue(result.is_success)
        self.assertEqual(result.trace.get_data(), "")
