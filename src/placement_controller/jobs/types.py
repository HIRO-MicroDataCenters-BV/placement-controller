class ActionResult:
    pass


ActionId = str

DEFAULT_TIMEOUT_SECONDS = 10


class Action:
    action_id: ActionId

    def __init__(self, action_id: ActionId):
        self.action_id = action_id

    def get_id(self) -> ActionId:
        return self.action_id

    def get_timeout_seconds(self) -> int:
        return DEFAULT_TIMEOUT_SECONDS

    async def run(self) -> ActionResult:
        raise NotImplementedError()
