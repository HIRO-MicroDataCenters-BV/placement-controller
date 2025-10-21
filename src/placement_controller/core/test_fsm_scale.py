import sys

from placement_controller.core.application import AnyApplication
from placement_controller.core.context import SchedulingContext
from placement_controller.core.fsm import FSM
from placement_controller.core.scheduling_state import FSMOperation, ScaleDirection, SchedulingState
from placement_controller.core.test_fsm_base import FSMTestBase
from placement_controller.core.types import SchedulingStep
from placement_controller.membership.types import PlacementZone


class FSMScaleTest(FSMTestBase):

    def setUp(self) -> None:
        super().setUp()

    def test_ordinary_placement(self) -> None:
        self.application = AnyApplication(
            self.make_anyapp(self.name.name, 1) | self.make_anyapp_status("Placement", "zone1", [])
        )
        operation = FSMOperation(
            direction=ScaleDirection.UPSCALE,
            required_replica=1,
            current_zones=set(),
            available_zones={"zone1", "zone2"},
        )

        # UNMANAGED state by default
        context = SchedulingContext.new(
            self.application, self.now, self.name, "zone1", [PlacementZone(id="zone1"), PlacementZone(id="zone2")]
        )
        self.assertEqual(context.state, SchedulingState.new(SchedulingStep.UNMANAGED, sys.maxsize - 60000))

        # PENDING and FETCH_APPLICATION_SPEC
        context = self.assert_fetch_application_spec(context, operation)

        # BID_COLLECTION
        context = self.assert_get_spec_to_bid_collection(context, operation, 60000)

        # DECISION
        context = self.assert_bid_collection_to_decision(
            context, operation, {"zone1": self.response1, "zone2": self.response2}, 60000
        )

        # SET_PLACEMENT
        context = self.assert_decision_to_placement(context, operation, [PlacementZone(id="zone1")], 60000)

        # PENDING
        self.assert_placements_done(context, 10000)

    def test_upscale(self) -> None:
        self.application = AnyApplication(
            self.make_anyapp(self.name.name, 2) | self.make_anyapp_status("Placement", "zone1", ["zone1"])
        )
        operation = FSMOperation(
            direction=ScaleDirection.UPSCALE,
            required_replica=2,
            current_zones={"zone1"},
            available_zones={"zone1", "zone2"},
        )

        # UNMANAGED state by default
        context = SchedulingContext.new(
            self.application, self.now, self.name, "zone1", [PlacementZone(id="zone1"), PlacementZone(id="zone2")]
        )
        self.assertEqual(context.state, SchedulingState.new(SchedulingStep.UNMANAGED, sys.maxsize - 60000))

        # PENDING and FETCH_APPLICATION_SPEC
        context = self.assert_fetch_application_spec(context, operation)

        # BID_COLLECTION
        context = self.assert_get_spec_to_bid_collection(context, operation, 60000)

        # DECISION
        context = self.assert_bid_collection_to_decision(
            context, operation, {"zone1": self.response1, "zone2": self.response2}, 60000
        )

        # SET_PLACEMENT
        context = self.assert_decision_to_placement(
            context, operation, [PlacementZone(id="zone1"), PlacementZone(id="zone2")], 60000
        )

        # PENDING
        self.assert_placements_done(context, 10000)

    def test_downscale(self) -> None:
        self.application = AnyApplication(
            self.make_anyapp(self.name.name, 1) | self.make_anyapp_status("Placement", "zone1", ["zone1", "zone2"])
        )
        operation = FSMOperation(
            direction=ScaleDirection.DOWNSCALE,
            required_replica=1,
            current_zones={"zone1", "zone2"},
            available_zones={"zone1", "zone2"},
        )

        # UNMANAGED state by default
        context = SchedulingContext.new(
            self.application, self.now, self.name, "zone1", [PlacementZone(id="zone1"), PlacementZone(id="zone2")]
        )
        self.assertEqual(context.state, SchedulingState.new(SchedulingStep.UNMANAGED, sys.maxsize - 60000))

        # PENDING and FETCH_APPLICATION_SPEC
        context = self.assert_fetch_application_spec(context, operation)

        # BID_COLLECTION
        context = self.assert_get_spec_to_bid_collection(context, operation, 60000)

        # DECISION
        context = self.assert_bid_collection_to_decision(
            context, operation, {"zone1": self.response1, "zone2": self.response2}, 60000
        )

        # SET_PLACEMENT
        context = self.assert_decision_to_placement(context, operation, [PlacementZone(id="zone1")], 60000)

        # PENDING
        self.assert_placements_done(context, 10000)

    def test_zone_failure(self) -> None:
        self.application = AnyApplication(
            self.make_anyapp(self.name.name, 2) | self.make_anyapp_status("Placement", "zone1", ["zone1", "zone2"])
        )
        operation = FSMOperation(
            direction=ScaleDirection.UPSCALE,
            required_replica=2,
            current_zones={"zone1", "zone2"},
            available_zones={"zone2", "zone3"},
        )

        # UNMANAGED state by default
        context = SchedulingContext.new(
            self.application, self.now, self.name, "zone1", [PlacementZone(id="zone2"), PlacementZone(id="zone3")]
        )
        self.assertEqual(context.state, SchedulingState.new(SchedulingStep.UNMANAGED, sys.maxsize - 60000))

        # PENDING and FETCH_APPLICATION_SPEC
        context = self.assert_fetch_application_spec(context, operation)

        # BID_COLLECTION
        context = self.assert_get_spec_to_bid_collection(context, operation, 60000)

        # DECISION
        context = self.assert_bid_collection_to_decision(
            context, operation, {"zone2": self.response2, "zone3": self.response3}, 60000
        )

        # SET_PLACEMENT
        context = self.assert_decision_to_placement(
            context, operation, [PlacementZone(id="zone2"), PlacementZone(id="zone3")], 60000
        )

        # PENDING
        self.assert_placements_done(context, 10000)

    def test_converge_after_failure(self) -> None:
        self.application = AnyApplication(
            self.make_anyapp(self.name.name, 2) | self.make_anyapp_status("Placement", "zone1", ["zone1"])
        )
        operation = FSMOperation(
            direction=ScaleDirection.UPSCALE,
            required_replica=2,
            current_zones={"zone1"},
            available_zones={"zone1", "zone2"},
        )

        # UNMANAGED state by default
        context = SchedulingContext.new(
            self.application, self.now, self.name, "zone1", [PlacementZone(id="zone1"), PlacementZone(id="zone2")]
        )
        self.assertEqual(context.state, SchedulingState.new(SchedulingStep.UNMANAGED, sys.maxsize - 60000))

        # PENDING and FETCH_APPLICATION_SPEC
        context = self.assert_fetch_application_spec(context, operation)

        # BID_COLLECTION
        context = self.assert_get_spec_to_bid_collection(context, operation, 60000)

        # DECISION
        context = self.assert_bid_collection_to_decision(
            context, operation, {"zone1": self.response2, "zone2": self.response3}, 60000
        )

        # SET_PLACEMENT
        context = self.assert_decision_to_placement(
            context, operation, [PlacementZone(id="zone1"), PlacementZone(id="zone2")], 60000
        )

        # PENDING
        self.assert_placements_done(context, 10000)

    def test_ignore_placement_if_pending_is_not_expired(self) -> None:
        self.application = AnyApplication(
            self.make_anyapp(self.name.name, 1) | self.make_anyapp_status("Operational", "zone1", ["zone1"])
        )

        self.now = 0
        # PENDING state
        context = SchedulingContext.new(
            self.application, self.now, self.name, "zone1", [PlacementZone(id="zone1"), PlacementZone(id="zone2")]
        )
        context.state = SchedulingState(
            SchedulingStep.PENDING, self.options.reschedule_default_delay_seconds * 1000, None
        )

        # tick does not expire pending state
        result = FSM(context, self.now, self.options).on_tick()
        self.assertIsNone(result.context)
        self.assertEqual(result.actions, [])

        self.now += 5000
        result = FSM(context, self.now, self.options).on_tick()
        self.assertIsNone(result.context)
        self.assertEqual(result.actions, [])

        # expired pending state
        self.now += 10001
        result = FSM(context, self.now, self.options).on_tick()

        operation = FSMOperation(
            direction=ScaleDirection.NONE,
            required_replica=1,
            current_zones={"zone1"},
            available_zones={"zone1", "zone2"},
        )

        if not result.context:
            raise self.fail("context expected")
        context = result.context
        action = result.actions[0]

        self.assertEqual(result.context.state, SchedulingState(SchedulingStep.FETCH_APPLICATION_SPEC, 75001, operation))
        self.assertEqual(action.name, self.name)

        # BID_COLLECTION
        context = self.assert_get_spec_to_bid_collection(context, operation, 75001)

        # DECISION
        context = self.assert_bid_collection_to_decision(
            context, operation, {"zone1": self.response1, "zone2": self.response2}, 75001
        )

        # SET_PLACEMENT
        context = self.assert_decision_to_placement(
            context, operation, [PlacementZone(id="zone1"), PlacementZone(id="zone2")], 75001
        )

        # PENDING
        self.assert_placements_done(context, 25001)

        # next tick - not expired
        self.now += 5000
        result = FSM(context, self.now, self.options).on_tick()
        self.assertIsNone(result.context)
        self.assertEqual(result.actions, [])
