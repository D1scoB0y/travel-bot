class BotError(Exception):
    def __init__(self, error: str) -> None:
        self.error = error
