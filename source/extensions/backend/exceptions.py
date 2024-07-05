from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

__all__ = ["DataBaseCompanyTextError"]


class DataBaseCompanyTextError(Exception):
    """
    Exception that is raised when a Telegram chat isn't private.
    """

    def __init__(self, message: str = "Error occurred when trying to get company text"):
        super().__init__(message)
