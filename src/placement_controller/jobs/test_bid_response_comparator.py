import functools
from decimal import Decimal
from unittest import TestCase

from placement_controller.api.model import (
    BidResponseModel,
    BidStatus,
    Metric,
    MetricUnit,
    MetricValue,
)
from placement_controller.jobs.decision_action import bid_response_comparator
from placement_controller.resource_fixture import ResourceTestFixture


class BidResponseComparatorTest(TestCase, ResourceTestFixture):

    response1: BidResponseModel
    response2: BidResponseModel
    response3: BidResponseModel

    def setUp(self) -> None:
        self.maxDiff = None

        self.response1 = BidResponseModel(
            id="test",
            status=BidStatus.accepted,
            metrics=[MetricValue(id=Metric.cost, value=Decimal("1.01"), unit=MetricUnit.eur)],
            reason=None,
            msg="OK",
        )
        self.response2 = BidResponseModel(
            id="test",
            status=BidStatus.accepted,
            metrics=[MetricValue(id=Metric.cost, value=Decimal("1.03"), unit=MetricUnit.eur)],
            reason=None,
            msg="OK",
        )
        self.response3 = BidResponseModel(
            id="test",
            status=BidStatus.accepted,
            metrics=[MetricValue(id=Metric.cost, value=Decimal("1.00"), unit=MetricUnit.eur)],
            reason=None,
            msg="OK",
        )
        self.criteria_priority = [Metric.cost, Metric.energy]

    def test_comparator(self) -> None:

        responses_including_current_zones = [
            ("zone1", self.response1),
            ("zone2", self.response2),
            ("zone3", self.response3),
        ]

        comparator = bid_response_comparator(self.criteria_priority)

        sorted_responses = sorted(
            responses_including_current_zones,
            key=functools.cmp_to_key(comparator),
        )

        self.assertEqual(
            [r[0] for r in sorted_responses],
            ["zone3", "zone1", "zone2"],
        )
