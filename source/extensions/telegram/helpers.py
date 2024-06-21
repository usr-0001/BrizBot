import asyncio
from typing import List

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import InlineKeyboardMarkup, Message, InputFile

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from source.extensions.database.database_queries import get_bot_messages_query
from source.extensions.telegram.event import Event
from source.persistance.models import BotMsg


__all__ = [
    "try_edit_message",
    "try_send_message",
    "try_send_photo",
    "try_edit_or_send_message",
    "try_delete_message_using_bot",
    "try_delete_message",
    "chat_isnt_private",
    "store_bot_msg",
    "delete_all_bot_messages"
]


_logger = logging.getLogger(__name__)


# region Send photo
async def try_send_photo(bot: Bot, chat_id: int, event_prefix: str, /, photo: InputFile | str, caption: str | None = None, reply_markup: InlineKeyboardMarkup | None = None) -> int:
    """
    Tries to send a photo.

    :param bot: The bot instance used to edit the message.
    :type bot: Bot


    :param chat_id: The id of the chat where the message is located.
    :type chat_id: int


    :param event_prefix: Prefix of the event to use in logs.
    :type event_prefix: str


    :param photo: File or Url of photo.
    :type photo: InputFile | str


    :param caption: The new text of the message, defaults to None.
    :type caption: str | None, optional


    :param reply_markup: The new inline keyboard markup for the message, defaults to None.
    :type reply_markup: InlineKeyboardMarkup | None, optional

    :return: The id of the new message.
    :rtype: int

    :raises TelegramForbiddenError: If the bot was blocked by the user or in any other case.
    :raises Exception: In any other error occurs in the core method.
    """

    try:
        message = await bot.send_photo(chat_id=chat_id, photo=photo, caption=caption, reply_markup=reply_markup)

    except TelegramForbiddenError as e:
        if (m := "bot was blocked by the user") in e.message:
            _logger.error(f"{event_prefix} {m}")
        raise

    else:
        return message.message_id

# endregion




# region Edit message
async def try_edit_message(bot: Bot, chat_id: int, message_id: int, event_prefix: str, /, text: str | None = None, markup: InlineKeyboardMarkup | None = None) -> bool:
    """
    Tries to edit a message.

    :param bot: The bot instance used to edit the message.
    :type bot: Bot

    :param chat_id: The id of the chat where the message is located.
    :type chat_id: int

    :param message_id: The id of the message to edit.
    :type message_id: int

    :param event_prefix: Prefix of the event to use in logs.
    :type event_prefix: str

    :param text: The new text of the message, defaults to None.
    :type text: str | None, optional

    :param markup: The new inline keyboard markup for the message, defaults to None.
    :type markup: InlineKeyboardMarkup | None, optional

    :return: True if the message was edited, False otherwise.
    :rtype: bool

    :raises TelegramForbiddenError: If the bot was blocked by the user.
    :raises TelegramBadRequest: In any other case except when the message content is the same or the message can't be edited.
    :raises Exception: In any other error occurs in the core method.
    """

    try:
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup)

    except TelegramForbiddenError as e:
        if (m := "bot was blocked by the user") in e.message:
            _logger.error(f"{event_prefix} {m}")

        else:
            raise

    except TelegramBadRequest as e:
        if (m := "specified new message content and reply markup are exactly the same as a current content and reply markup of the message") in e.message:
            _logger.warning(f"{event_prefix} message {message_id} {m}")
            return True

        elif (m := "message can't be edited") in e.message:
            _logger.error(f"{event_prefix} message {message_id} {m}")
            return False

        elif (m := "message to edit not found") in e.message:
            _logger.error(f"{event_prefix} message {message_id} {m}")
            return False

        else:
            raise

    else:
        return True

# endregion


# region Send / Edit message
async def try_send_message(bot: Bot, chat_id: int, event_prefix: str, /, text: str | None = None, markup: InlineKeyboardMarkup | None = None) -> int:
    """
    Tries to send a message.

    :param bot: The bot instance used to send the message.
    :type bot: Bot

    :param chat_id: The id of the chat where the message will be sent.
    :type chat_id: int

    :param event_prefix: Prefix of the event to use in logs.
    :type event_prefix: str

    :param text: The text of the message, defaults to None.
    :type text: str | None, optional

    :param markup: The inline keyboard markup for the message, defaults to None.
    :type markup: InlineKeyboardMarkup | None, optional

    :return: The id of the new message.
    :rtype: int

    :raises TelegramForbiddenError: If the bot was blocked by the user or in any other case.
    :raises Exception: In any other error occurs in the core method.
    """

    try:
        message = await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)

    except TelegramForbiddenError as e:
        if (m := "bot was blocked by the user") in e.message:
            _logger.error(f"{event_prefix} {m}")
        raise

    else:
        return message.message_id


async def try_edit_or_send_message(bot: Bot, chat_id: int, message_id: int, event_prefix: str, /, text: str | None = None, markup: InlineKeyboardMarkup | None = None) -> int:
    """
    Tries to edit a message. If it fails, sends a new message and updates the chat view's telegram_id.

    :param bot: The bot instance used to edit or send the message.
    :type bot: Bot

    :param chat_id: The id of the chat where the message will be sent.
    :type chat_id: int

    :param message_id: The id of the message to edit.
    :type message_id: int

    :param event_prefix: Prefix of the event to use in logs.
    :type event_prefix: str

    :param text: The text of the message, defaults to None.
    :type text: str | None, optional

    :param markup: The inline keyboard markup for the message, defaults to None.
    :type markup: InlineKeyboardMarkup | None, optional

    :return: The id of the existing or new message.
    :rtype: int

    :raises TelegramForbiddenError: If the bot was blocked by the user or in any other case.
    :raises TelegramBadRequest: If the message can't be edited or in any other case.
    :raises Exception: In any other error occurs in the core method.
    """

    if await try_edit_message(bot, chat_id, message_id, event_prefix, text=text, markup=markup) is not True:
        _logger.warning(f"{event_prefix} message {message_id} can't be edited so new message will be sent")
        return await try_send_message(bot, chat_id, event_prefix, text=text, markup=markup)

    else:
        return message_id

# endregion


# region Delete message
async def try_delete_message_using_bot(bot: Bot, chat_id: int, message_id: int, event: Event) -> bool:
    """
    Tries to delete a message.

    :param bot: The bot instance used to delete the message.
    :type bot: Bot

    :param chat_id: The id of the chat where the message will be deleted.
    :type chat_id: int

    :param message_id: Id of the message to delete.
    :type message_id: int

    :param event: Prefix of the event to use in logs.
    :type event: Event

    :return: True if the message was deleted, False otherwise.
    :rtype: bool

    :raises TelegramForbiddenError: In any other case except when the bot was blocked by the user.
    :raises TelegramBadRequest: In any other case except when the message can't be found.
    :raises Exception: In any other error occurs in the core method.
    """

    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)

    except TelegramForbiddenError as e:
        if (m := "bot was blocked by the user") in e.message:
            _logger.error(f"{event.prefix} {m}")
            return False

        else:
            raise

    except TelegramBadRequest as e:
        if (m := "message to delete not found") in e.message:
            _logger.error(f"{event.prefix} message {message_id} {m}")
            return False

        elif (m := "message can't be deleted for everyone") in e.message:
            _logger.error(f"{event.prefix} message {message_id} {m}")
            return False

        else:
            raise

    else:
        return True


async def _get_all_bot_messages(session: AsyncSession, chat_id: int) -> List[BotMsg]:
    """
    This function retrieves all bot messages from the database for a specific chat.

    :param session: A database session.
    :type session: AsyncSession

    :param chat_id: The ID of the chat.
    :type chat_id: BigInteger

    :returns: Objects representing bot messages.
    :rtype: List[BotMsg]
    """

    query_result = await session.execute(get_bot_messages_query(chat_id=chat_id))
    bot_messages = query_result.scalars().all()
    return bot_messages


async def delete_all_bot_messages(bot: Bot, chat_id: int, event_prefix: str, session: AsyncSession):
    """
    This function deletes all bot messages in a chat using the provided bot instance.

    :param bot: The bot instance used to delete the message.
    :type bot: Bot

    :param chat_id: The ID of the chat.
    :type chat_id: int

    :param event_prefix: A prefix for event handling.
    :type event_prefix: str

    :param session: A database session.
    :type session: AsyncSession

    :returns: Objects representing bot messages.
    :rtype: List[BotMsg]
    """

    # Get messages from database/
    bot_messages: list[BotMsg] = await _get_all_bot_messages(session=session, chat_id=chat_id)

    # Delete messages.
    for message in bot_messages:
        # Delete from chat.
        await try_delete_message_using_bot(bot, chat_id, message.message_id, event_prefix)
        # Delete from database.
        await session.delete(message)


async def try_delete_message(message: Message, event: Event) -> bool:
    """
    Tries to delete a message using a Message object.

    :param message: The message object containing chat ID and message ID.
    :type message: Message

    :param event: Prefix of the event to use in logs.
    :type event: Event

    :return: True if the message was deleted, False otherwise.
    :rtype: bool

    :raises TelegramForbiddenError: In any other case except when the bot was blocked by the user.
    :raises TelegramBadRequest: In any other case except when the message can't be found.
    :raises Exception: In any other error occurs in the core method.
    """

    return await try_delete_message_using_bot(bot=message.bot, chat_id=message.chat.id, message_id=message.message_id, event=event)

# endregion


def chat_isnt_private(event: Event) -> bool:
    """
    Checks if the telegram chat isn't private.

    :param event: The event data.
    :return: True, if the chat isn't private, False, otherwise.
    """

    return True if event.chat_type != "private" or event.chat_id != event.user_id else False


async def store_bot_msg(chat_id: int, message_id: int, session: AsyncSession):
    """
    Add new bot msg id in database.

    :param chat_id: The id of the chat where the message was sent.
    :type chat_id: int

    :param message_id: The id of the message.
    :type message_id: int

    :param session: Database session.
    :type session: AsyncSession
    """

    bot_msg = BotMsg(chat_id=chat_id, message_id=message_id)
    session.add(bot_msg)



