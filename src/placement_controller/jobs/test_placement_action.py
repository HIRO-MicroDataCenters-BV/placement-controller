from typing import Any, Dict, List

from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.clients.k8s.fake_client import FakeClient
from placement_controller.core.application import AnyApplication
from placement_controller.jobs.placement_action import PlacementDecision, SetPlacementAction
from placement_controller.jobs.types import ExecutorContext
from placement_controller.membership.types import PlacementZone
from placement_controller.resource_fixture import ResourceTestFixture
from placement_controller.store.fake_decision_store import FakeDecisionStore
from placement_controller.util.mock_clock import MockClock
from placement_controller.zone.types import ZoneApiFactory


class SetPlacementActionTest(AsyncTestFixture, ResourceTestFixture):
    decision_store: FakeDecisionStore
    client: FakeClient
    name: NamespacedName
    action: SetPlacementAction

    zones: List[PlacementZone]
    decision: PlacementDecision
    app: Dict[str, Any]

    def setUp(self) -> None:
        super().setUp()
        self.clock = MockClock()
        self.decision_store = FakeDecisionStore()
        self.client = FakeClient()
        self.name = NamespacedName(name="test", namespace="test")

        self.app = self.make_anyapp(self.name.name, 1) | self.make_anyapp_status("state", "owner", [])

        self.zones = [PlacementZone(id="zone1"), PlacementZone(id="zone2"), PlacementZone(id="zone3")]
        self.context = ExecutorContext(
            application_controller_client=None,  # type: ignore
            zone_api_factory=ZoneApiFactory(),
            kube_client=self.client,
            clock=self.clock,
            decision_store=self.decision_store,
        )
        self.decision = PlacementDecision(
            spec="{}",
            placements=self.zones,
            reason="reason",
            trace="trace",
        )
        self.action = SetPlacementAction(self.decision, self.name, "test")

    def tearDown(self) -> None:
        super().tearDown()

    def test_set_placement(self) -> None:
        self.loop.run_until_complete(self.client.patch(AnyApplication.GVK, self.app))

        result = self.loop.run_until_complete(self.action.run(self.context))
        self.assertTrue(result.result)

        updated_dict: Dict[str, Any] = self.loop.run_until_complete(
            self.client.get(AnyApplication.GVK, self.name)  # type: ignore
        )
        self.assertEqual(AnyApplication(updated_dict).get_placement_zones(), ["zone1", "zone2", "zone3"])
