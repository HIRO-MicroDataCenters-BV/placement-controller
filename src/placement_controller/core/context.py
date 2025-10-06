from placement_controller.core.application import AnyApplication
from placement_controller.core.types import SchedulingState


class SchedulingContext:
    application: AnyApplication
    state: SchedulingState

    def __init__(self, state: SchedulingState, application: AnyApplication):
        self.state = state
        self.application = application
