from typing import Tuple

from sqlalchemy import select, cast, BigInteger, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from source.extensions.backend.exceptions import DataBaseCompanyTextError
from source.persistance.models import Chat, User, CompanyText, BotMsg

__all__ = ["get_chat_query", "get_user_query"]


def get_bot_messages_query(chat_id: int):
    query = select(BotMsg).where(BotMsg.chat_id == cast(chat_id, BigInteger))
    return query


async def get_chat(id: int, session: AsyncSession, include_user: bool = False, include_view: bool = False, lock: bool = False) -> Chat | None:
    """
    Gets the Chat.

    :param id: The telegram id.
    :param session: The database session.
    :param include_user: Whether to include the User related to the Chat.
    :param include_view: Whether to include the View related to the Chat.
    :param lock: Whether to apply a FOR UPDATE NOWAIT lock on the chat.
    :return: Chat or None.
    """

    return (await session.execute(get_chat_query(id, include_user, include_view, lock))).scalars().first()


def get_chat_query(id: int, include_user: bool = False, include_view: bool = False, lock: bool = False) -> Select[Tuple[Chat]]:
    """
    Constructs a query to fetch a Chat.

    :param id: The telegram id of the chat.
    :type id: int

    :param include_user: Whether to include the User related to the Chat, defaults to False.
    :type include_user: bool, optional

    :param include_view: Whether to include the View related to the Chat, defaults to False.
    :type include_view: bool, optional

    :param lock: Whether to apply a FOR UPDATE NOWAIT lock on the chat, defaults to False.
    :type lock: bool, optional

    :return: A query to fetch the Chat.
    :rtype: Select[Tuple[Chat]]
    """

    query = select(Chat).where(Chat.id == cast(id, BigInteger))

    if include_user is True: query = query.options(joinedload(Chat.user))
    # if include_view is True: query = query.options(joinedload(Chat.kind_id))
    if lock is True: query = query.with_for_update(of=Chat, nowait=True)

    query = query.order_by(Chat.id)
    return query


async def get_user(id: int, session: AsyncSession, include_chat: bool = False, lock: bool = False) -> Chat | None:
    """
    Gets the User.

    :param id: The telegram id.
    :param session: The database session.
    :param include_chat: Whether to include the Chat related to the User.
    :param lock: Whether to apply a FOR UPDATE NOWAIT lock on the chat.
    :return: User or None.
    """

    return (await session.execute(get_user_query(id, include_chat, lock))).scalars().first()


def get_user_query(id: int, include_chat: bool = False, lock: bool = False) -> Select[Tuple[User]]:
    """
    Constructs a query to fetch a User.

    :param id: The telegram id of the user.
    :type id: int

    :param include_chat: Whether to include the Chat related to the User, defaults to False.
    :type include_chat: bool, optional

    :param lock: Whether to apply a FOR UPDATE NOWAIT lock on the user, defaults to False.
    :type lock: bool, optional

    :return: A query to fetch the User.
    :rtype: Select[Tuple[User]]
    """

    query = select(User).where(User.telegram_id == cast(id, BigInteger))

    if include_chat is True: query = query.options(joinedload(User.chat))
    if lock is True: query = query.with_for_update(of=User, nowait=True)

    return query


async def get_company_text(kind_id: int, session: AsyncSession) -> str:
    """
    Gets the text from database.

    :param kind_id:
    :param session:
    :return: Text from database filtered by kind_id from TextKindVariant enum
    """

    company_text: CompanyText | None = (await session.execute(get_company_text_query(kind_id))).scalars().first()
    if company_text is None: raise DataBaseCompanyTextError()

    return company_text.text


def get_company_text_query(text_id: int):
    """
    Constructs a query to fetch a Chat.

    :param text_id: The id of the text in database.
    :type text_id: int

    :return: A query to fetch the Chat.
    :rtype: Select[Tuple[CompanyText]]
    """

    query = select(CompanyText).where(CompanyText.id == cast(text_id, BigInteger))
    return query