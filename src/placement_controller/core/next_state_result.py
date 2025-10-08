from typing import List, Optional

from dataclasses import dataclass, field

from placement_controller.core.context import SchedulingContext
from placement_controller.jobs.types import Action, ActionResult


@dataclass
class NextStateResult:
    actions: List[Action[ActionResult]] = field(default_factory=list)
    context: Optional[SchedulingContext] = field(default=None)
