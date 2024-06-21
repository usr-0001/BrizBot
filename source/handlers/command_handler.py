from typing import Type, cast

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select, cast, BigInteger, Select
from sqlalchemy import BigInteger
from sqlalchemy.ext.asyncio import AsyncSession

import logging
from source import context
from source.extensions.backend.backend_exceptions import DataBaseCompanyTextError
from source.extensions.telegram.markup import TelegramMarkup
from source.extensions.telegram.exceptions import TelegramNonPrivateChatError

from source.extensions.telegram.event import EventData
from source.extensions.database.database_queries import get_chat_query, get_user_query, get_company_text_query
from source.extensions.telegram.helpers import telegram_chat_is_not_private, try_send_message, store_bot_msg, \
    delete_all_bot_messages, try_delete_message, try_send_photo
from source.persistance.models import *
from source.extensions.telegram.objects import bot
from source.persistance.models import TextKindVariant

router = Router(name=__name__)
_logger = logging.getLogger(__name__)
__all__ = ["router"]


def _on_command(function):
    """
    Provides wrapper for each command handler.
    """

    async def wrapper(message: Message) -> None:
        """
        Handles command.
        """

        event = EventData(
            bot=message.bot,
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            chat_type=message.chat.type,
            message_id=message.message_id,
            message_text=message.text,
            prefix=f"Chat {message.chat.id} command {message.message_id} '{message.text}'"
        )

        try:
            _logger.info(f"{event.prefix} has been accepted")
            if telegram_chat_is_not_private(event): raise TelegramNonPrivateChatError()
            async with context.session() as session: await function(message, session, event)

        except TelegramNonPrivateChatError as e:
            _logger.error(f"{event.prefix} chat isn't private")

        except Exception as e:
            _logger.error(f"{event.prefix} hasn't been processed correctly", exc_info=e)

        else:
            _logger.info(f"{event.prefix} has been processed")

        finally:
            await try_delete_message(message, event.prefix)

    return wrapper


@router.message(CommandStart(ignore_case=True))
@_on_command
async def _on_start(message: Message, session: AsyncSession, event: EventData) -> None:
    """
    Handles start.
    """

    chat: Chat | None = (await session.execute(get_chat_query(id=event.chat_id, include_user=True, include_view=True, lock=True))).scalars().first()

    # Creates the chat.
    if chat is None:

        # Gets the user.
        user: User | None = (await session.execute(get_user_query(id=event.user_id))).scalars().first()

        # Creates the user.
        if user is None:
            _logger.warning(f"{event.prefix} user {event.user_id} doesn't exist and will be created")
            user = User(
                telegram_id=event.user_id,
                chat_id=event.chat_id,
                is_active_in_telegram=True,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                username=message.from_user.username,
                phone=None
            )

        _logger.warning(f"{event.prefix} chat {event.chat_id} doesn't exist and will be created")
        chat = Chat(id=event.chat_id)
        chat.user = [user]
        session.add(chat)

    # Resets states.
    # Chat.
    chat.kind_id = ViewKindVariant.MAIN_MENU.value
    chat.content = None
    chat.sub_window_number = 1

    # Create user window.
    # Send start message to user.\
    company_text: CompanyText | None = (await session.execute(get_company_text_query(TextKindVariant.BOT_COMMAND_START.value))).scalars().first()
    if company_text is None: raise DataBaseCompanyTextError()

    message_id = await try_send_photo(
        bot,
        event.chat_id,
        event.prefix,
        photo='http://briz-berdyansk.com/images/briz.png',
        caption=company_text.text,
        reply_markup=TelegramMarkup.main_menu()

    )

    # Delete all previously bot messages and store new message.
    await delete_all_bot_messages(
        bot=bot,
        chat_id=event.chat_id,
        event_prefix=event.prefix,
        session=session
    )
    await store_bot_msg(chat_id=event.chat_id, message_id=message_id, session=session)

    # Saves changes.
    await session.commit()
