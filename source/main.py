import asyncio

from aiogram.types import BotCommand

from source import settings, context
from source.handlers import router as handlers_router
from source.extensions.telegram.objects import bot, dispatcher

import logging

from source.handlers.dispather import on_startup, on_shutdown


async def main() -> None:
    """
    Starts the application.
    """
    try:
        # Bot.
        commands = [BotCommand(command=c.name, description=c.description) for c in settings.bot.commands]
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_my_commands(commands)

        # Dispatcher.
        dispatcher.startup.register(on_startup)
        dispatcher.shutdown.register(on_shutdown)
        dispatcher.include_router(handlers_router)
        await dispatcher.start_polling(bot)

    except Exception as e:
        _logger.error("An unexpected error has occurred", exc_info=e)

    finally:
        await context.close()


if __name__ == "__main__":
    _logger = logging.getLogger(__name__)
    _logger.info("Application has been started")

    asyncio.run(main())  # Run the main function when the script is executed directly
    _logger.info("Application has been shut down")

