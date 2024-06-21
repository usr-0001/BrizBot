__all__ = [
    "TelegramNonPrivateChatException",
    "TelegramBotIsBlockedByUserException"
]



class TelegramNonPrivateChatException(Exception):
    """Exception that is raised when a Telegram chat isn't private."""

    def __init__(self, message: str = "Telegram chat isn't private"):
        super().__init__(message)



class TelegramBotIsBlockedByUserException(Exception):
    """Exception that is raised when a Telegram bot is blocked by a user."""

    def __init__(self, message: str = "Telegram bot is blocked by a user"):
        super().__init__(message)

