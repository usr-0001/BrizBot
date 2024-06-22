from functools import wraps

from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

import logging
from source import context, settings
from source.extensions.backend.exceptions import DataBaseCompanyTextError
from source.extensions.database.query import get_chat, get_user

from source.extensions.telegram.event import Event
from source.extensions.telegram.exceptions import TelegramNonPrivateChatException, TelegramBotIsBlockedByUserException
from source.extensions.telegram.helpers import chat_isnt_private, try_delete_message, try_send_photo, store_bot_msg, \
    delete_all_bot_messages, try_delete_message_using_bot
from source.extensions.telegram.markup import TelegramMarkup
from source.extensions.telegram.objects import bot
from source.extensions.telegram.windows import load_main_window
from source.persistance.models import User, Chat, ViewKindVariant, CompanyText, TextKindVariant


__all__ = ["router"]


router = Router(name=__name__)
_logger = logging.getLogger(__name__)


def on_command(function):
    """Provides wrapper for command handler."""

    @wraps(function)
    async def wrapper(message: Message) -> None:
        """Handles command."""

        event = Event(
            bot=message.bot,
            user_id=message.from_user.id,
            chat_id=message.chat.id, chat_type=message.chat.type,
            message_id=message.message_id, message_text=message.text,
            prefix=f"event (chat '{message.chat.id}', command '{message.message_id}', text '{message.text}')"
        )

        try:
            _logger.info(f"{event.prefix} has been accepted")
            if chat_isnt_private(event): raise TelegramNonPrivateChatException()

            async with context.session() as session:
                await function(message, session, event)
                await session.commit()

        except TelegramNonPrivateChatException:
            _logger.error(f"{event.prefix} chat isn't private")

        except TelegramBotIsBlockedByUserException:
            _logger.error(f"{event.prefix} bot is blocked by the user")

        except Exception as e:
            _logger.error(f"{event.prefix} hasn't been processed correctly", exc_info=e)

        else:
            _logger.info(f"{event.prefix} has been processed")

        finally:
            await try_delete_message_using_bot(bot, event.chat_id, message.message_id, event)

    return wrapper


@router.message(CommandStart(ignore_case=True))
@on_command
async def _on_start(message: Message, session: AsyncSession, event: Event) -> None:
    """
    Handles start.
    """

    # Gets the chat.
    chat = await get_chat(event.chat_id, session, include_user=True, include_view=True, lock=True)

    # Creates the chat.
    if not chat:
        # Gets the user.
        user = await get_user(event.user_id, session)

        # Creates the user.
        if not user:
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

    await load_main_window(chat=chat, event=event, session=session)


