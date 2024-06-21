# import inspect
# from functools import wraps, partial
#
# from aiogram import Router
# import logging
#
# from source.extensions.telegram.event import Event
#
# from aiogram.types import CallbackQuery
#
# from source import settings
#
#
# router = Router(name=__name__)
# _logger = logging.getLogger(__name__)
# _popup_settings = settings.popup
# __all__ = ["router"]
#
#
# def on_button(function):
#     """Provides wrapper for button handler."""
#
#     @wraps(function)
#     async def wrapper(query: CallbackQuery) -> None:
#         """Handles button."""
#
#         event = Event(
#             bot=query.bot,
#             user_id=query.from_user.id,
#             chat_id=query.message.chat.id, chat_type=query.message.chat.type,
#             message_id=query.message.message_id, message_text=query.message.text,
#             prefix=f"event (chat '{query.message.chat.id}', message '{query.message.message_id}', button '{query.data}')"
#         )
#
#         try:
#             _logger.info(f"{event.prefix} has been accepted")
#             if chat_isnt_private(event): raise TelegramNonPrivateChatException()
#
#             async with context.session() as session:
#                 await function(query, session, event)
#                 await session.commit()
#
#         except PropertyNotFoundException as e:
#             _logger.error(f"{event.prefix} Property {e.property} isn't found")
#             await try_answer_query(query, event, _popup_settings.error)
#
#         except TelegramNonPrivateChatException:
#             _logger.error(f"{event.prefix} chat isn't private")
#             await try_answer_query(query, event, _popup_settings.error)
#
#         except TelegramBotIsBlockedByUserException:
#             _logger.error(f"{event.prefix} bot is blocked by the user")
#             await try_answer_query(query, event, _popup_settings.error)
#
#         except TelegramForbiddenError as e:
#             if not try_guard_blocked_bot_FALLBACK(e, event): raise
#             await try_answer_query(query, event, _popup_settings.error)
#
#         except TelegramBadRequest as e:
#             if not try_guard_expired_or_invalid_query_FALLBACK(e, event): raise
#
#         except DBAPIError as e:
#             if not try_guard_database_lock(e, event): raise
#             await try_answer_query(query, event, _popup_settings.error)
#
#         except Exception as e:
#             _logger.error(f"{event.prefix} hasn't been processed correctly", exc_info=e)
#             await try_answer_query(query, event, _popup_settings.error)
#
#         else:
#             _logger.info(f"{event.prefix} has been processed")
#
#         finally:
#             pass
#
#     return wrapper