from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from dataclasses import dataclass, field
from datetime import datetime, timezone

from aiogram import Bot


__all__ = ["Event"]


@dataclass(frozen=True)
class Event:
    """
    A class to represent the event data of a Telegram bot.

    :param bot: The bot.
    :type bot: Bot

    :param user_id: The id of the user.
    :type user_id: int

    :param chat_id: The id of the chat.
    :type chat_id: int

    :param chat_type: The type of the chat (e.g., private, group, supergroup, channel).
    :type chat_type: str

    :param message_id: The id of the message, if any (default is None).
    :type message_id: int | None

    :param message_text: The text content of the message, if any (default is None).
    :type message_text: str | None

    :param prefix: The string representation of the event, if any (default is None).
    :type prefix: str | None
    """

    bot: Bot
    user_id: int
    chat_id: int
    chat_type: str
    message_id: int | None = None
    message_text: str | None = None
    prefix: str | None = None
    utc_now: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
