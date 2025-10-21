from typing import Any, Optional, Set

import sys
from dataclasses import dataclass
from enum import StrEnum

from placement_controller.core.types import SchedulingStep

DEFAULT_RESCHEDULE_DELAY_SECONDS: int = 60 * 60
DEFAULT_FAILURE_DELAY_SECONDS: int = 60
DEFAULT_STEP_EXPIRATION_SECONDS: int = 60


class ScaleDirection(StrEnum):
    UPSCALE = "upscale"
    DOWNSCALE = "downscale"
    NONE = "none"


@dataclass
class FSMOperation:
    direction: ScaleDirection
    required_replica: int
    current_zones: Set[str]
    available_zones: Set[str]


class SchedulingState:
    step: SchedulingStep
    expires_at: int
    operation: Optional[FSMOperation]

    def __init__(self, step: SchedulingStep, expires_at: int, operation: Optional[FSMOperation]):
        self.step = step
        self.expires_at = expires_at
        self.operation = operation

    @staticmethod
    def initial(timestamp: int) -> "SchedulingState":
        return SchedulingState(SchedulingStep.UNMANAGED, sys.maxsize, None)

    def start_operation(self, timestamp: int, operation: FSMOperation) -> "SchedulingState":
        return SchedulingState(
            SchedulingStep.PENDING,
            timestamp + DEFAULT_STEP_EXPIRATION_SECONDS * 1000,
            operation,
        )

    @staticmethod
    def new(step: SchedulingStep, now_timestamp: int) -> "SchedulingState":
        return SchedulingState(step, now_timestamp + DEFAULT_STEP_EXPIRATION_SECONDS * 1000, None)

    def to(self, step: SchedulingStep, now_timestamp: int) -> "SchedulingState":
        return SchedulingState(step, now_timestamp + DEFAULT_STEP_EXPIRATION_SECONDS * 1000, self.operation)

    def is_expired(self, now_timestamp: int) -> bool:
        return self.expires_at < now_timestamp

    def is_expired_state(self, step: SchedulingStep, now_timestamp: int) -> bool:
        return self.step == step and self.expires_at < now_timestamp

    def is_valid_at(self, step: SchedulingStep, now_timestamp: int) -> bool:
        return self.step == step and now_timestamp < self.expires_at

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SchedulingState):
            raise NotImplementedError
        return self.step == other.step and self.expires_at == other.expires_at and self.operation == other.operation

    def __str__(self) -> str:
        direction = self.operation.direction if self.operation else ScaleDirection.NONE
        return f"{self.step}@{{direction={direction}, expires_at={self.expires_at}}}"
