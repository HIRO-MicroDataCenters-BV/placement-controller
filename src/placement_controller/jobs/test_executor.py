import asyncio

from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.clients.k8s.fake_client import FakeClient
from placement_controller.core.async_queue import AsyncQueue
from placement_controller.jobs.executor import JobExecutor
from placement_controller.jobs.types import Action, ActionId, ActionResult, ExecutorContext


class FakeActionResult(ActionResult):
    result: int

    def __init__(self, result: int, name: NamespacedName, action_id: ActionId):
        super().__init__(name, action_id)
        self.result = result


class FakeAction(Action[FakeActionResult]):
    result: int

    def __init__(self, result: int, name: NamespacedName, action_id: ActionId):
        super().__init__(name, action_id)
        self.result = result

    async def run(self, context: ExecutorContext) -> FakeActionResult:
        return FakeActionResult(self.result, self.name, self.action_id)


class JobExecutorTest(AsyncTestFixture):

    actions: AsyncQueue[Action[FakeActionResult]]
    results: AsyncQueue[FakeActionResult]

    executor: JobExecutor
    executor_context: ExecutorContext
    terminated: asyncio.Event
    loop: asyncio.AbstractEventLoop

    name: NamespacedName

    def setUp(self) -> None:
        super().setUp()
        self.actions = AsyncQueue[Action[FakeActionResult]]()
        self.results = AsyncQueue[FakeActionResult]()
        self.name = NamespacedName(name="test", namespace="testns")

        self.executor_context = ExecutorContext(
            application_controller_client=None,  # type: ignore
            zone_api_factory=None,  # type: ignore
            kube_client=FakeClient(),
        )
        self.executor = JobExecutor(self.executor_context, self.actions, self.results, self.terminated)  # type: ignore

        self.task = self.loop.create_task(self.executor.run())

    def tearDown(self) -> None:
        self.task.cancel()
        super().tearDown()

    def test_execute_job_and_get_result(self) -> None:
        action = FakeAction(1, self.name, "1")
        expected = FakeActionResult(1, self.name, "1")

        self.actions.put_nowait(action)

        def action_result_check() -> bool:
            action_result = self.results.get_nowait()
            if action_result:
                return action_result.get_application_name() == expected.name and action_result.result == expected.result
            else:
                return False

        self.wait_for_condition(2, action_result_check)
