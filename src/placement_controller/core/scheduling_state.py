from typing import Any

from enum import StrEnum

from placement_controller.core.types import SchedulingStep

DEFAULT_RESCHEDULE_DELAY_SECONDS: int = 60 * 60
DEFAULT_FAILURE_DELAY_SECONDS: int = 60
DEFAULT_STEP_EXPIRATION_SECONDS: int = 60


class ScheduleFlowType(StrEnum):
    UPSCALE = "upscale"
    DOWNSCALE = "downscale"


class SchedulingState:
    step: SchedulingStep
    expires_at: int
    flow_type: ScheduleFlowType

    def __init__(self, step: SchedulingStep, expires_at: int):
        self.step = step
        self.expires_at = expires_at
        self.flow_type = ScheduleFlowType.UPSCALE

    @staticmethod
    def start(timestamp: int) -> "SchedulingState":
        return SchedulingState(SchedulingStep.PENDING, timestamp + DEFAULT_STEP_EXPIRATION_SECONDS * 1000)

    @staticmethod
    def new(step: SchedulingStep, now_timestamp: int) -> "SchedulingState":
        return SchedulingState(step, now_timestamp + DEFAULT_STEP_EXPIRATION_SECONDS * 1000)

    def is_valid_at(self, step: SchedulingStep, now_timestamp: int) -> bool:
        return self.step == step and now_timestamp < self.expires_at

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SchedulingState):
            raise NotImplementedError
        return self.step == other.step and self.expires_at == other.expires_at and self.flow_type == other.flow_type

    def __str__(self) -> str:
        return f"{self.step}@{{flow={self.flow_type}, expires_at={self.expires_at}}}"
