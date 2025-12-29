from typing import Any, Dict

import json

from application_client.models.application_spec import ApplicationSpec

from placement_controller.api.model import BidRequestModel, BidResponseModel, BidStatus, TraceLogRowModel
from placement_controller.clients.k8s.client import KubeClient
from placement_controller.resources.placement import GreedyPlacement
from placement_controller.resources.trace_log import TraceLog
from placement_controller.resources.types import ResourceManagement, ResourceMetrics, ResourceTracking
from placement_controller.util.clock import Clock


class ResourceManagementImpl(ResourceManagement):
    zone: str
    clock: Clock
    client: KubeClient
    resource_tracking: ResourceTracking
    resource_metrics: ResourceMetrics

    def __init__(
        self,
        zone: str,
        clock: Clock,
        client: KubeClient,
        resource_tracking: ResourceTracking,
        resource_metrics: ResourceMetrics,
    ):
        self.zone = zone
        self.client = client
        self.clock = clock
        self.resource_tracking = resource_tracking
        self.resource_metrics = resource_metrics

    def application_bid(self, bid: BidRequestModel) -> BidResponseModel:
        nodes = self.resource_tracking.list_nodes()
        app_spec: Dict[str, Any] = json.loads(bid.spec)
        spec = ApplicationSpec.from_dict(app_spec)
        name = bid.name.to_domain()
        trace_log = TraceLog(self.zone, name, clock=self.clock)
        placement = GreedyPlacement(trace_log, nodes, spec, bid.bid_criteria)

        result = placement.try_place()
        status = BidStatus.accepted if result.is_success() else BidStatus.rejected

        estimates = self.resource_metrics.estimate(spec, list(bid.metrics))
        trace_rows = [TraceLogRowModel.from_domain(log_row) for log_row in result.trace.get_raw()]
        return BidResponseModel(
            id=bid.id,
            status=status,
            reason=result.reason,
            trace=trace_rows,
            metrics=estimates,
        )
