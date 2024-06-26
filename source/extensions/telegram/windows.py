import logging

from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from source import settings
from source.extensions.database.query import get_room_by_id
from source.extensions.telegram.event import Event
from source.extensions.telegram.helpers import delete_all_bot_messages, store_bot_msg, try_send_photo
from source.extensions.telegram.markup import TelegramMarkup
from source.extensions.telegram.objects import bot
from source.persistance.models import ViewKindVariant, Chat


_logger = logging.getLogger(__name__)


async def load_main_window(chat: Chat, event: Event, session: AsyncSession):
    # Update states.
    current_kind_id = chat.kind_id

    text = settings.view.screen.main_menu.text
    chat.kind_id = ViewKindVariant.MAIN_MENU_WINDOW.value
    chat.content = text
    chat.sub_window_number = 1

    markup = TelegramMarkup.main_menu()

    if current_kind_id is ViewKindVariant.SHOW_ROOMS_AND_PRICES_WINDOW.value:
        room = await get_room_by_id(id=chat.sub_window_number, session=session)

        await bot.edit_message_media(
            chat_id=event.chat_id,
            message_id=event.message_id,
            media=InputMediaPhoto(
                media=room.preview_img_url,
                caption=text
            ),
            reply_markup=markup
        )
        return

    # Send start message to user.
    message_id = await try_send_photo(
        bot,
        event.chat_id,
        event,
        photo=settings.view.screen.main_menu.photo_url,
        caption=chat.content,
        reply_markup=markup
    )
    # Delete all previously bot messages and store new message.
    await delete_all_bot_messages(
        bot=bot,
        chat_id=event.chat_id,
        event=event,
        session=session
    )
    await store_bot_msg(chat_id=event.chat_id, message_id=message_id, session=session)


async def load_room_and_prices_window(chat: Chat, event: Event, session: AsyncSession):
    # Gets the Room.
    room = await get_room_by_id(id=chat.sub_window_number, session=session)

    # Create markup.
    _logger.warning(f'chat.sub_window_number is {chat.sub_window_number}')
    list_back = True if chat.sub_window_number > 1 else False
    list_forward = True if chat.sub_window_number < settings.view.screen.rooms_and_prices_menu.rooms_count else False
    markup = TelegramMarkup.navigate_between_items(list_forward=list_forward, list_back=list_back)

    # Send start message to user.
    text = f'{room.name}\n\n{room.description}\n\n{room.price_text}'
    chat.content = text

    await bot.edit_message_media(
        chat_id=event.chat_id,
        message_id=event.message_id,
        media=InputMediaPhoto(
            media=room.preview_img_url,
            caption=text
        ),
        reply_markup=markup
    )
