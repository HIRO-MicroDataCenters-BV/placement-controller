from typing import List

from dataclasses import dataclass, field


@dataclass
class TraceLog:
    data: List[str] = field(default_factory=list)

    def log(self, msg: str) -> None:
        self.data.append(msg)

    def get_raw(self) -> List[str]:
        return self.data

    def get_data(self) -> str:
        return "\n".join(self.data)
