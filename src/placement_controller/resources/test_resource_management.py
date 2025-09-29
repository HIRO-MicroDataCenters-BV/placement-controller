from asyncio import Task

from placement_controller.api.model import BidRequestModel, BidResponseModel, BidStatus
from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.k8s.fake_client import FakeClient
from placement_controller.resource_fixture import ResourceTestFixture
from placement_controller.resources.resource_managment import ResourceManagement
from placement_controller.resources.resource_tracking import ResourceTrackingImpl
from placement_controller.resources.types import ResourceTracking


class ResourceManagementTest(AsyncTestFixture, ResourceTestFixture):
    client: FakeClient
    tracking: ResourceTracking
    resource_management: ResourceManagement
    task: Task[None]

    def setUp(self) -> None:
        super().setUp()
        self.client = FakeClient()

        self.tracking = ResourceTrackingImpl(self.client, self.terminated)
        self.task = self.loop.create_task(self.tracking.start())
        self.wait_for_condition(2, lambda: self.tracking.is_subscription_active())

        self.resource_management = ResourceManagement(self.client, self.tracking)

    def tearDown(self) -> None:
        self.task.cancel()
        super().tearDown()

    def test_application_bid(self):
        bid = BidRequestModel(id="id", spec="", bid_criteria=set(), metrics=set())
        response = self.resource_management.application_bid(bid)
        self.assertEqual(
            response, BidResponseModel(id=bid.id, status=BidStatus.rejected, reason=None, msg=None, metrics=[])
        )
