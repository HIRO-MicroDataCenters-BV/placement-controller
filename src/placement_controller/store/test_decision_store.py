from orchestrationlib_client.client import Client

from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.k8s.client import NamespacedName
from placement_controller.resource_fixture import ResourceTestFixture
from placement_controller.store.decision_store import DecisionStoreImpl
from placement_controller.store.fake_orchestrationlib_server import FakeOrchestrationlibServer


class DecisionStoreImplTest(AsyncTestFixture, ResourceTestFixture):
    fake_server: FakeOrchestrationlibServer
    store: DecisionStoreImpl

    name: NamespacedName

    def setUp(self) -> None:
        super().setUp()

        self.fake_server = FakeOrchestrationlibServer(host="127.0.0.1")
        self.fake_server.start()
        self.wait_for_condition(2, lambda: self.fake_server.is_available())

        client = Client(base_url=self.fake_server.get_base_url())
        self.store = DecisionStoreImpl(client)

        self.name = NamespacedName(name="test", namespace="test")
        self.spec = """{ "test":"test" }"""

    def tearDown(self) -> None:
        self.fake_server.stop()
        super().tearDown()

    def test_save_decision(self) -> None:
        response = self.loop.run_until_complete(
            self.store.save(self.name, self.spec, ["zone1", "zone2"], "reason", "trace", 0)
        )
        print(response)
