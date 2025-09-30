from typing import List


class TraceLog:
    data: List[str]

    def __init__(self):
        self.data = []

    def log(self, msg: str) -> None:
        self.data.append(msg)

    def get_raw(self) -> List[str]:
        return self.data

    def get_data(self) -> str:
        return "\n".join(self.data)
