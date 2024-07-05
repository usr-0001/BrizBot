from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from source import settings
from source.extensions.telegram.isolation import UserChatIsolation

__all_ = ["dispatcher", "bot"]


dispatcher = Dispatcher(events_isolation=UserChatIsolation())
bot = Bot(token=settings.bot.token, default=DefaultBotProperties(parse_mode=settings.bot.parse_mode))
