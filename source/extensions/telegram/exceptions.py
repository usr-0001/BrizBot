__all__ = ["TelegramNonPrivateChatError"]


class TelegramNonPrivateChatError(Exception):
    """
    Exception that is raised when a Telegram chat isn't private.
    """

    def __init__(self, message: str = "Telegram chat isn't private"):
        super().__init__(message)
