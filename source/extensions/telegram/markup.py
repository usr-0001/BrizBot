from os import path
import sys

from source.handlers.PhotoGalery import photo_gallery
from source.handlers.VideoGalery import video_gallery
from source.persistance.models import ViewKindVariant

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import cast, String

from source.extensions.telegram.callbacks import *
from source import settings

__all__ = ["TelegramMarkup"]

from source.extensions.telegram.callbacks import NavigationMenuButtonData, NavigationMenuButtonAction


_logger = logging.getLogger(__name__)


class TelegramMarkup:
    __none: InlineKeyboardMarkup | None = None
    __main_menu: InlineKeyboardMarkup | None = None
    __load_prev: InlineKeyboardMarkup | None = None
    #__navigate_between_items: InlineKeyboardMarkup | None = None

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
            url='https://www.youtube.com/@briz_pirat_themed_guest_house'
        )
        builder.button(
            text=texts.admins_button,
            callback_data=MainMenuButtonData(action=MainMenuButtonAction.SHOW_ADMINS_WINDOW)
        )
        builder.button(
            text=texts.map_button,
            callback_data=MainMenuButtonData(action=MainMenuButtonAction.SHOW_MAP_WINDOW)
        )
        builder.button(
            text=texts.food_button,
            callback_data=MainMenuButtonData(action=MainMenuButtonAction.SHOW_FOOD_WINDOW)
        )

        builder.adjust(2, 2, 1, 1, 1)
        markup = builder.as_markup()

        cls.__main_menu = markup
        return markup

    @classmethod
    def navigate_between_items(cls, list_back: bool, list_forward: bool, chat = None) -> InlineKeyboardMarkup:
        #if cls.__navigate_between_items: return cls.__navigate_between_items

        builder = InlineKeyboardBuilder()

        forward_text = settings.view.screen.navigation.list_forward
        if chat is not None:
            if chat.kind_id is ViewKindVariant.SHOW_PHOTO_GALLERY_WINDOW.value:
                forward_text = f"Ещё {int(photo_gallery.length()-chat.sub_window_number*5)} фото "+settings.view.screen.navigation.list_forward
            if chat.kind_id is ViewKindVariant.SHOW_ROOMS_AND_PRICES_WINDOW.value:
                rooms_available = settings.view.screen.rooms_and_prices_menu.rooms_count-chat.sub_window_number
                postfix = ''
                match rooms_available:
                    case 1: postfix = 'комната'
                    case 2: postfix = 'комнаты'
                    case 3: postfix = 'комнаты'
                    case 4: postfix = 'комнаты'
                    case 5: postfix = 'комнат'
                    case 6: postfix = 'комнат'
                    case 7: postfix = 'комнат'
                    case 8: postfix = 'комнат'
                    case 9: postfix = 'комнат'

                forward_text = f"Ещё {settings.view.screen.rooms_and_prices_menu.rooms_count-chat.sub_window_number} {postfix} "+settings.view.screen.navigation.list_forward

        if list_back:
            builder.button(
                text=settings.view.screen.navigation.list_back,
                callback_data=NavigationMenuButtonData(action=NavigationMenuButtonAction.LIST_BACK)
            )
        if list_forward:
            builder.button(
                text=forward_text,
                callback_data=NavigationMenuButtonData(action=NavigationMenuButtonAction.LIST_FORWARD)
            )
        builder.button(
            text=settings.view.screen.navigation.load_prev_menu,
            callback_data=NavigationMenuButtonData(action=NavigationMenuButtonAction.LOAD_PREV_MENU)
        )

        sizes = [2 if (list_forward is True and list_back is True) else 1, 1]
        builder.adjust(*sizes, repeat=False)
        markup = builder.as_markup()

        return markup


    @classmethod
    def load_prev_window(cls) -> InlineKeyboardMarkup:
        if cls.__load_prev: return cls.__load_prev

        builder = InlineKeyboardBuilder()
        builder.button(
            text=settings.view.screen.navigation.load_prev_menu,
            callback_data=NavigationMenuButtonData(action=NavigationMenuButtonAction.LOAD_PREV_MENU)
        )

        builder.adjust(1)
        markup = builder.as_markup()

        cls.__load_prev = markup
        return markup
