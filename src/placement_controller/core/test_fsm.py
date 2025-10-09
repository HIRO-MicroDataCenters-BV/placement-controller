import unittest

from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.application import AnyApplication
from placement_controller.core.context import SchedulingContext
from placement_controller.core.fsm import FSM
from placement_controller.resource_fixture import ResourceTestFixture


class FSMTest(unittest.TestCase, ResourceTestFixture):

    name: NamespacedName
    application: AnyApplication

    def setUp(self) -> None:
        self.name = NamespacedName(name="test", namespace="testns")
        self.application = AnyApplication(self.make_anyapp("nginx", 1))

    def test_new_application(self) -> None:
        context = SchedulingContext.new(1)

        result = FSM(context, 1).next_state(self.application)

        self.assertEqual(result.actions, [])
        # self.assertEqual(result.context.state, SchedulingState.NEW)
