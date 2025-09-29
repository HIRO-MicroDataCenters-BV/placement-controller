class TraceLog:
    data: str

    def __init__(self):
        self.data = ""

    def log(self, msg: str) -> None:
        self.data += msg + "\n"

    def get_data(self) -> str:
        return self.data
