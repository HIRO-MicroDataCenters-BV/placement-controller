from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.core.scheduling_queue import SchedulingQueue


class SchedulingQueueTest:
    queue: SchedulingQueue
    name: NamespacedName

    def setUp(self) -> None:
        self.name = NamespacedName(name="test", namespace="testns")
        self.queue = SchedulingQueue()

    def test_schedule(self) -> None:
        pass
