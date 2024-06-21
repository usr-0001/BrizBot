from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from source.extensions.telegram.callbacks import *
from source import settings


__all__ = ["TelegramMarkup"]


class TelegramMarkup:
    __none: InlineKeyboardMarkup | None = None
    __main_menu: InlineKeyboardMarkup | None = None

    @classmethod
    def none(cls) -> InlineKeyboardMarkup | None:
        if cls.__none: return cls.__none

        markup = None

        cls.__none = markup
        return markup

    @classmethod
    def main_menu(cls) -> InlineKeyboardMarkup:
        if cls.__main_menu: return cls.__main_menu

        texts = settings.view.screen.main_menu
        builder = InlineKeyboardBuilder()
        builder.button(
            text=texts.rooms_and_prices_button,
            callback_data=MainMenuButtonData(action=MainMenuButtonAction.SHOW_ROOMS_AND_PRICES_WINDOW)
        )
        builder.button(
            text=texts.room_reservation_button,
            callback_data=MainMenuButtonData(action=MainMenuButtonAction.SHOW_ROOM_RESERVATION_WINDOW)
        )
        builder.button(
            text=texts.photo_gallery_button,
            callback_data=MainMenuButtonData(action=MainMenuButtonAction.SHOW_PHOTO_GALLERY_WINDOW)
        )
        builder.button(
            text=texts.video_gallery_button,
            callback_data=MainMenuButtonData(action=MainMenuButtonAction.SHOW_VIDEO_GALLERY_WINDOW)
        )
        builder.button(
            text=texts.admins_button,
            callback_data=MainMenuButtonData(action=MainMenuButtonAction.SHOW_ADMINS_WINDOW)
        )
        builder.button(
            text=texts.map.button,
            callback_data=MainMenuButtonData(action=MainMenuButtonAction.SHOW_MAP_WINDOW)
        )

        builder.adjust(2, 2, 1, 1)
        markup = builder.as_markup()

        cls.__main_menu = markup
        return markup
