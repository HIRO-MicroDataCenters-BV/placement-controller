from placement_controller.core.application import AnyApplication
from placement_controller.core.context import SchedulingContext
from placement_controller.core.fsm import FSM
from placement_controller.core.scheduling_state import FSMOperation, ScaleDirection, SchedulingState
from placement_controller.core.test_fsm_base import FSMTestBase
from placement_controller.core.types import SchedulingStep
from placement_controller.jobs.bid_action import BidAction
from placement_controller.jobs.decision_action import DecisionAction
from placement_controller.jobs.get_spec_action import GetSpecAction
from placement_controller.jobs.placement_action import SetPlacementAction
from placement_controller.membership.types import PlacementZone


class FSMFailureTest(FSMTestBase):

    def setUp(self) -> None:
        super().setUp()

    def test_action_timeouts_and_retries(self) -> None:
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
            self.application, self.now, self.name, [PlacementZone(id="zone1"), PlacementZone(id="zone2")]
        )
        self.assertEqual(context.state, SchedulingState.new(SchedulingStep.UNMANAGED, self.now))

        # PENDING and FETCH_APPLICATION_SPEC
        context = self.assert_fetch_application_spec(context, operation)
        context = self.assert_retry(context, SchedulingStep.FETCH_APPLICATION_SPEC, operation, GetSpecAction)

        # BID_COLLECTION
        context = self.assert_get_spec_to_bid_collection(context, operation, 120001)
        context = self.assert_retry(context, SchedulingStep.BID_COLLECTION, operation, BidAction)

        # DECISION
        context = self.assert_bid_collection_to_decision(
            context, operation, {"zone1": self.response1, "zone2": self.response2}, 180002
        )
        context = self.assert_retry(context, SchedulingStep.DECISION, operation, DecisionAction)

        # SET_PLACEMENT
        context = self.assert_decision_to_placement(context, operation, [PlacementZone(id="zone1")], 240003)
        context = self.assert_retry(context, SchedulingStep.SET_PLACEMENT, operation, SetPlacementAction)

        # PENDING
        self.assert_placements_done(context, 250004)

    def test_unmanaged_managed(self) -> None:
        self.application = AnyApplication(
            self.make_anyapp(self.name.name, 1) | self.make_anyapp_status("Placement", "zone2", ["zone2"])
        )

        # UNMANAGED state by default
        context = SchedulingContext.new(
            self.application, self.now, self.name, [PlacementZone(id="zone1"), PlacementZone(id="zone2")]
        )
        self.assertEqual(context.state, SchedulingState.new(SchedulingStep.UNMANAGED, self.now))

        # Application register
        result = FSM(context, self.current_zone, self.now, self.options).on_update(self.application)
        if result.context is None:
            self.fail("context expected")
        context = result.context

        self.assertEqual(context.state.step, SchedulingStep.UNMANAGED)
        self.assertEqual(context.application.object, self.application.object)

        # application update to managed

        self.application.set_owner_zone("zone1")
        self.application.object["spec"]["zones"] = 2

        result = FSM(context, self.current_zone, self.now, self.options).on_update(self.application)
        if result.context is None:
            self.fail("context expected")
        context = result.context

        # starting placement lifecycle
        self.assertEqual(context.state.step, SchedulingStep.FETCH_APPLICATION_SPEC)
        self.assertEqual(context.application.object, self.application.object)

    def test_update_during_operation(self) -> None:
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
            self.application, self.now, self.name, [PlacementZone(id="zone1"), PlacementZone(id="zone2")]
        )
        self.assertEqual(context.state, SchedulingState.new(SchedulingStep.UNMANAGED, self.now))

        # PENDING and FETCH_APPLICATION_SPEC
        context = self.assert_fetch_application_spec(context, operation)
        self.assert_application_update(context, SchedulingStep.FETCH_APPLICATION_SPEC, operation)

        # BID_COLLECTION
        context = self.assert_get_spec_to_bid_collection(context, operation, 60000)
        self.assert_application_update(context, SchedulingStep.BID_COLLECTION, operation)

        # DECISION
        context = self.assert_bid_collection_to_decision(
            context, operation, {"zone1": self.response1, "zone2": self.response2}, 60000
        )
        self.assert_application_update(context, SchedulingStep.DECISION, operation)

        # SET_PLACEMENT
        context = self.assert_decision_to_placement(
            context, operation, [PlacementZone(id="zone1"), PlacementZone(id="zone2")], 60000
        )
        self.assert_application_update(context, SchedulingStep.SET_PLACEMENT, operation)

        # PENDING
        context = self.assert_placements_done(context, 10000)

        operation.required_replica = 3
        operation = FSMOperation(
            direction=ScaleDirection.UPSCALE,
            required_replica=7,
            current_zones={"zone1"},
            available_zones={"zone1", "zone2"},
        )
        self.assert_application_update(context, SchedulingStep.FETCH_APPLICATION_SPEC, operation)
