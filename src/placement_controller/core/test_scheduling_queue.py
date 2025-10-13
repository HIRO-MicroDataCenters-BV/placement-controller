import unittest

from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.scheduling_queue import SchedulingQueue
from placement_controller.util.mock_clock import MockClock


class SchedulingQueueTest(unittest.TestCase):
    clock: MockClock
    queue: SchedulingQueue
    name: NamespacedName

    def setUp(self) -> None:
        self.name = NamespacedName(name="test", namespace="testns")
        self.clock = MockClock()
        self.queue = SchedulingQueue(self.clock, "zone1")

    def test_schedule(self) -> None:
        # TODO tests
        pass
