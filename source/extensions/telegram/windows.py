from sqlalchemy.ext.asyncio import AsyncSession

from source import settings
from source.extensions.telegram.event import Event
from source.extensions.telegram.helpers import delete_all_bot_messages, store_bot_msg, try_send_photo
from source.extensions.telegram.markup import TelegramMarkup
from source.extensions.telegram.objects import bot
from source.persistance.models import ViewKindVariant, Chat


async def load_main_window(chat: Chat, event: Event, session: AsyncSession):
    # Update states.
    text = settings.view.screen.main_menu.text
    chat.kind_id = ViewKindVariant.MAIN_MENU_WINDOW.value
    chat.content = text
    chat.sub_window_number = 1

    # Send start message to user.
    message_id = await try_send_photo(
        bot,
        event.chat_id,
        event,
        photo=settings.view.screen.main_menu.photo_url,
        caption=chat.content,
        reply_markup=TelegramMarkup.main_menu()
    )
    # Delete all previously bot messages and store new message.
    await delete_all_bot_messages(
        bot=bot,
        chat_id=event.chat_id,
        event=event,
        session=session
    )
    await store_bot_msg(chat_id=event.chat_id, message_id=message_id, session=session)
