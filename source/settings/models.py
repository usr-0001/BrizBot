from typing import List
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

__all__ = ["Settings"]


# region Logging
class LoggingConsole(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    level: str
    template: str


class LoggingFile(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    level: str
    template: str
    directory: str
    name: str


class LoggingSettings(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    level: str
    console: LoggingConsole
    file: LoggingFile


# endregion


# region Backend
class Backend(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    url: str
    img_path: str


# endregion


# region Persistence
class Database(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    connection_string: str
    connection_timeout: int
    logging_level: str


class PersistenceSettings(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    database: Database


# endregion


# region Bot
class BotCommand(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    name: str
    description: str


class BotSettings(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    token: str
    parse_mode: str
    commands: List[BotCommand]


# endregion


# region View
class MainMenu(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    photo_url: str
    text: str
    rooms_and_prices_button: str
    room_reservation_button: str
    photo_gallery_button: str
    video_gallery_button: str
    admins_button: str
    map_button: str


class RoomsAndPricesMenu(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    rooms_count: int


class Contact(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    name: str
    phone: str


class AdminMenu(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    text: str
    contacts: list[Contact]


class MapMenu(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    text: str
    latitude: float
    longitude: float


class Navigation(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    list_back: str
    list_forward: str
    load_prev_menu: str


class Screen(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    main_menu: MainMenu
    rooms_and_prices_menu: RoomsAndPricesMenu
    admin_menu: AdminMenu
    map_menu: MapMenu
    navigation: Navigation


class View(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    screen: Screen


# enregion


# Root
class Settings(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    logging: LoggingSettings
    persistence: PersistenceSettings
    bot: BotSettings
    view: View
