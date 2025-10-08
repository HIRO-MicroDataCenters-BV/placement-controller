from typing import Optional

from placement_controller.core.application import AnyApplication
from placement_controller.core.types import SchedulingState


class SchedulingContext:
    application: Optional[AnyApplication]
    state: SchedulingState

    def __init__(self, state: SchedulingState):
        self.state = state
        self.application = None
