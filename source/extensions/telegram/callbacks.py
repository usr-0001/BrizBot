from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from enum import Enum
from aiogram.filters.callback_data import CallbackData

__all__ = [
    "MainMenuButtonAction",
    "MainMenuButtonData"
]


# region RoomsAndPricesButton
class MainMenuButtonAction(Enum):
    """Room and prices button action."""

    SHOW_ROOMS_AND_PRICES_WINDOW = 'SHOW_ROOMS_AND_PRICES_WINDOW'
    SHOW_ROOM_RESERVATION_WINDOW = 'SHOW_ROOM_RESERVATION_WINDOW'
    SHOW_SAUNA_WINDOW = 'SHOW_SAUNA_WINDOW'
    SHOW_PHOTO_GALLERY_WINDOW = 'SHOW_PHOTO_GALLERY_WINDOW'
    SHOW_VIDEO_GALLERY_WINDOW = 'SHOW_VIDEO_GALLERY_WINDOW'
    SHOW_ADMINS_WINDOW = 'SHOW_ADMINS_WINDOW'
    SHOW_MAP_WINDOW = 'SHOW_MAP_WINDOW'
    SHOW_FOOD_WINDOW = 'SHOW_FOOD_WINDOW'


class MainMenuButtonData(CallbackData, prefix="MainMenu"):
    """
    Data for RoomsAndPrices button callback data.

    :ivar action: The associated action.
    """

    action: MainMenuButtonAction
# region


# region NavigationButton
class NavigationMenuButtonAction(Enum):
    LIST_BACK = 'LIST_BACK'
    LIST_FORWARD = 'LIST_FORWARD'
    LOAD_PREV_MENU = 'LOAD_PREV_MENU'


class NavigationMenuButtonData(CallbackData, prefix="NavigationMenu"):
    action: NavigationMenuButtonAction
# endregion
