from pathlib import Path

from logging import getLogger
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from source.settings.loader import load_settings
from source.logging.configuration import create_console_handler, create_file_handler, configure_logging
from source.persistance.database import DatabaseContext

_APP_PATH = Path(__file__).resolve().parent
__all__ = ["settings", "context"]

# Settings
settings = load_settings(_APP_PATH / "appsettings.json")

# Logging
configure_logging(handlers=
[
    create_console_handler(
        template=settings.logging.console.template,
        level=settings.logging.console.level
    ),
    create_file_handler(
        template=settings.logging.file.template,
        file_path=_APP_PATH / settings.logging.file.directory / settings.logging.file.name,
        level=settings.logging.file.level
    )
], level=settings.logging.level)

# Persistence
getLogger("sqlalchemy.engine").setLevel(settings.persistence.database.logging_level)
context = DatabaseContext(
    settings.persistence.database.connection_string,
    connect_args={
        "connect_timeout": settings.persistence.database.connection_timeout,
        "echo": False
    }
)

