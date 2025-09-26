from placement_controller.api.model import BidRequestModel, BidResponseModel, BidStatus
from placement_controller.async_fixture import AsyncTestFixture
from placement_controller.clients.k8s.fake_client import FakeClient
from placement_controller.resource_fixture import ResourceTestFixture
from placement_controller.resources.resource_managment import ResourceManagement
from placement_controller.resources.resource_tracking import ResourceTrackingImpl


class ResourceManagementTest(AsyncTestFixture, ResourceTestFixture):
    client: FakeClient
    resource_management: ResourceManagement

    def setUp(self) -> None:
        super().setUp()

        self.client = FakeClient()
        self.resource_management = ResourceManagement(self.client, ResourceTrackingImpl(self.client, self.terminated))

    def tearDown(self):
        return super().tearDown()

    def test_application_bid(self):
        bid = BidRequestModel(id="id", spec="", bid_criteria=[], metrics=[])
        response = self.resource_management.application_bid(bid)
        self.assertEqual(
            response, BidResponseModel(id=bid.id, status=BidStatus.rejected, reason=None, msg=None, metrics=[])
        )
