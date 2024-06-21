from aiogram import Dispatcher
import logging


_logger = logging.getLogger(__name__)
__all__ = ["on_startup", "on_shutdown"]


async def on_startup(dispatcher: Dispatcher):
    """
    Handles dispatcher startup event.
    """

    

    _logger.info("Dispatcher has been started")


async def on_shutdown(dispatcher: Dispatcher):
    """
    Handles dispatcher shutdown event.
    """

    _logger.info("Dispatcher has been shut down")
