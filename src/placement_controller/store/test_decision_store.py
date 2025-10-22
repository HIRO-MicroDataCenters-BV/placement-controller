from orchestrationlib_client.client import Client

from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.resource_fixture import ResourceTestFixture
from placement_controller.store.decision_store import DecisionStoreImpl
from placement_controller.store.fake_orchestrationlib_server import FakeOrchestrationlibServer


class DecisionStoreImplTest(AsyncTestFixture, ResourceTestFixture):
    fake_server: FakeOrchestrationlibServer
    store: DecisionStoreImpl

    def setUp(self) -> None:
        super().setUp()

        self.fake_server = FakeOrchestrationlibServer("127.0.0.1")

        client = Client(base_url=self.fake_server.get_base_url())
        self.store = DecisionStoreImpl(client)

    def tearDown(self) -> None:
        super().tearDown()

    def test_save_decision(self) -> None:
        pass
