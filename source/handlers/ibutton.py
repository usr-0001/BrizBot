import inspect
from functools import wraps, partial

from aiogram import Router, F
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from source.extensions.backend.exceptions import DataBaseCompanyTextError
from source.extensions.database.query import get_chat, get_company_text_query, get_company_text
from source.extensions.telegram.callbacks import MainMenuButtonAction, MainMenuButtonData
from source.extensions.telegram.event import Event

from aiogram.types import CallbackQuery

from source import settings, context

__all__ = ["router"]

from source.extensions.telegram.exceptions import TelegramNonPrivateChatException

from source.extensions.telegram.helpers import chat_isnt_private
from source.extensions.telegram.objects import bot
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
    """Handles activation start."""

    # Gets the chat.
    chat = await get_chat(event.chat_id, session, include_user=True, include_view=True, lock=True)

    # Update states.
    text = await get_company_text(kind_id=TextKindVariant.IBUTTON_MAP.value, session=session)
    chat.kind_id = ViewKindVariant.MAIN_MENU_WINDOW.value
    chat.content = text
    chat.sub_window_number = 1

    await bot.send_location(
        chat_id=event.chat_id,
        latitude=settings.view.screen.main_menu.map.latitude,
        longitude=settings.view.screen.main_menu.map.longitude

    )






















