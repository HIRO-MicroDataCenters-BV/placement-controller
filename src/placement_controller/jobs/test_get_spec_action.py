import asyncio

from application_client import models
from application_client.client import Client

from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.jobs.fake_application_controller import FakeApplicationController
from placement_controller.jobs.get_spec_action import GetSpecAction
from placement_controller.resource_fixture import ResourceTestFixture


class GetSpecActionTest(AsyncTestFixture, ResourceTestFixture):

    terminated: asyncio.Event
    loop: asyncio.AbstractEventLoop
    server: FakeApplicationController

    name: NamespacedName
    client: Client
    action: GetSpecAction
    spec: models.ApplicationSpec

    def setUp(self) -> None:
        super().setUp()
        self.name = NamespacedName(name="test", namespace="testns")
        self.spec = models.ApplicationSpec(
            id=models.ResourceId(name="test", namespace="test"),
            resources=[self.make_pod_spec("pod1", 1, {"cpu": "2", "memory": "200Mi"}, {})],
        )

        self.server = FakeApplicationController(host="127.0.0.1")
        self.server.mock_response(self.spec)
        self.server.start()

        self.client = Client(base_url=self.server.get_base_url())
        self.action = GetSpecAction(self.client, self.name, "test")
        self.wait_for_condition(2, lambda: self.server.is_available())

    def tearDown(self) -> None:
        super().tearDown()
        self.server.stop()

    def test_get_app_spec(self) -> None:
        result = self.loop.run_until_complete(self.action.run())
        self.assertEqual(result.response, self.spec)
