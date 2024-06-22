import inspect
from functools import wraps, partial

from aiogram import Router, F
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from source.extensions.backend.exceptions import DataBaseCompanyTextError
from source.extensions.database.query import get_chat
from source.extensions.telegram.callbacks import MainMenuButtonAction, MainMenuButtonData, NavigationMenuButtonData, \
    NavigationMenuButtonAction
from source.extensions.telegram.event import Event

from aiogram.types import CallbackQuery

from source import settings, context

__all__ = ["router"]

from source.extensions.telegram.exceptions import TelegramNonPrivateChatException

from source.extensions.telegram.helpers import chat_isnt_private, delete_all_bot_messages, store_bot_msg, \
    try_send_message, get_all_bot_messages, try_delete_message, try_edit_or_send_message, try_send_photo
from source.extensions.telegram.markup import TelegramMarkup
from source.extensions.telegram.objects import bot
from source.extensions.telegram.windows import load_main_window
from source.persistance.models import ViewKindVariant, CompanyText, TextKindVariant

router = Router(name=__name__)
_logger = logging.getLogger(__name__)


def on_button(function):
    """Provides wrapper for button handler."""

    @wraps(function)
    async def wrapper(query: CallbackQuery) -> None:
        """Handles button."""

        event = Event(
            bot=query.bot,
            user_id=query.from_user.id,
            chat_id=query.message.chat.id, chat_type=query.message.chat.type,
            message_id=query.message.message_id, message_text=query.message.text,
            prefix=f"event (chat '{query.message.chat.id}', message '{query.message.message_id}', button '{query.data}')"
        )

        try:
            _logger.info(f"{event.prefix} has been accepted")
            if chat_isnt_private(event): raise TelegramNonPrivateChatException()

            async with context.session() as session:
                await function(query, session, event)
                await session.commit()

        except TelegramNonPrivateChatException:
            _logger.error(f"{event.prefix} chat isn't private")

        except Exception as e:
            _logger.error(f"{event.prefix} hasn't been processed correctly", exc_info=e)

        else:
            _logger.info(f"{event.prefix} has been processed")

        finally:
            pass

    return wrapper


@router.callback_query(MainMenuButtonData.filter(F.action == MainMenuButtonAction.SHOW_MAP_WINDOW))
@on_button
async def on_show_map_window(query: CallbackQuery, session: AsyncSession, event: Event):
    # Gets the chat.
    chat = await get_chat(event.chat_id, session, include_user=True, include_view=True, lock=True)

    # Update states.
    text = settings.view.screen.map_menu.text
    chat.kind_id = ViewKindVariant.SHOW_MAP_WINDOW.value
    chat.content = text
    chat.sub_window_number = 1

    message_id = await try_send_message(
        bot,
        event.chat_id,
        event,
        text=chat.content
    )

    map_message_id = (await bot.send_location(
        chat_id=event.chat_id,
        latitude=settings.view.screen.map_menu.latitude,
        longitude=settings.view.screen.map_menu.longitude,
        reply_markup=TelegramMarkup.load_prev_window()
    )).message_id

    # Delete all previously bot messages and store new message.
    await delete_all_bot_messages(
        bot=bot,
        chat_id=event.chat_id,
        event=event,
        session=session
    )
    await store_bot_msg(chat_id=event.chat_id, message_id=message_id, session=session)
    await store_bot_msg(chat_id=event.chat_id, message_id=map_message_id, session=session)


@router.callback_query(MainMenuButtonData.filter(F.action == MainMenuButtonAction.SHOW_ADMINS_WINDOW))
@on_button
async def on_show_admins_window(query: CallbackQuery, session: AsyncSession, event: Event):
    # Gets the chat.
    chat = await get_chat(event.chat_id, session, include_user=True, include_view=True, lock=True)

    # Update states.
    # text = settings.view.screen._menu.text
    chat.kind_id = ViewKindVariant.SHOW_ADMINS_WINDOW.value
    chat.content = settings.view.screen.admin_menu.text
    chat.sub_window_number = 1

    message_id = await try_send_message(
        bot,
        event.chat_id,
        event,
        text=chat.content
    )

    contact_1_message_id = (await bot.send_contact(
        chat_id=event.chat_id,
        phone_number=settings.view.screen.admin_menu.contacts[0].phone,
        first_name=settings.view.screen.admin_menu.contacts[0].name
    )).message_id
    contact_2_message_id = (await bot.send_contact(
        chat_id=event.chat_id,
        phone_number=settings.view.screen.admin_menu.contacts[1].phone,
        first_name=settings.view.screen.admin_menu.contacts[1].name,
        reply_markup=TelegramMarkup.load_prev_window()
    )).message_id

    # Delete all previously bot messages and store new message.
    await delete_all_bot_messages(
        bot=bot,
        chat_id=event.chat_id,
        event=event,
        session=session
    )
    await store_bot_msg(chat_id=event.chat_id, message_id=message_id, session=session)
    await store_bot_msg(chat_id=event.chat_id, message_id=contact_1_message_id, session=session)
    await store_bot_msg(chat_id=event.chat_id, message_id=contact_2_message_id, session=session)


@router.callback_query(NavigationMenuButtonData.filter(F.action == NavigationMenuButtonAction.LOAD_PREV_MENU))
@on_button
async def on_load_prev_window(query: CallbackQuery, session: AsyncSession, event: Event):
    # Gets the chat.
    chat = await get_chat(event.chat_id, session, include_user=True, include_view=True, lock=True)

    match chat.kind_id:
        case ViewKindVariant.SHOW_MAP_WINDOW.value | ViewKindVariant.SHOW_ADMINS_WINDOW.value:
            await load_main_window(chat=chat, event=event, session=session)
