from asyncio import Lock
from collections import defaultdict
from contextlib import asynccontextmanager
from typing import DefaultDict, Hashable, AsyncGenerator

from aiogram.fsm.storage.base import StorageKey, BaseEventIsolation


__all__ = ["UserChatIsolation"]


class UserChatIsolation(BaseEventIsolation):
    """
    Event isolation implementation that manages locks based on user and chat ids.
    This ensures that messages from the same user and chat are processed sequentially,
    while allowing concurrency between different users or chats.

    :ivar _locks: A dictionary of asyncio locks indexed by a tuple of (user_id, chat_id).
    """

    def __init__(self) -> None:
        """Initializes the instance."""
        self._locks: DefaultDict[Hashable, Lock] = defaultdict(Lock)

    @asynccontextmanager
    async def lock(self, key: StorageKey) -> AsyncGenerator[None, None]:
        """
        Acquires a lock based on the provided StorageKey.

        :param key: The storage key containing data to be locked.
        :yield: None
        """

        lock = self._locks[(key.user_id, key.chat_id)]
        async with lock:
            yield

    async def close(self) -> None:
        """Closes the isolation strategy by clearing all existing locks."""
        self._locks.clear()


