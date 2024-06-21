import os

from logging import handlers as logging_handlers
from pathlib import Path
from typing import Iterable

import logging
from .formatters import ColorfulConsoleFormatter


def create_console_handler(template: str, level: str = logging.DEBUG) -> logging.StreamHandler:
    """
    Creates a console logging handler with colored output.

    :param template: The log message format string.
    :type template: str

    :param level: The logging level. Defaults to logging.DEBUG.
    :type level: str

    :return: A configured StreamHandler with colorful console output.
    :rtype: logging.StreamHandler
    """

    handler = logging.StreamHandler()
    handler.setFormatter(ColorfulConsoleFormatter(fmt=template))
    handler.setLevel(level)

    return handler


def create_file_handler(template: str, file_path: Path, level: str = logging.DEBUG) -> logging_handlers.TimedRotatingFileHandler:
    """
    Creates a file logging handler that rotates at midnight.

    :param template: The log message format string.
    :type template: str

    :param file_path: The path to the log file.
    :type file_path: Path

    :param level: The logging level. Defaults to logging.DEBUG.
    :type level: str

    :return: A configured TimedRotatingFileHandler.
    :rtype: logging_handlers.TimedRotatingFileHandler
    """

    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    handler = logging_handlers.TimedRotatingFileHandler(filename=file_path, when="midnight", interval=1, utc=True)
    handler.setFormatter(logging.Formatter(fmt=template))
    handler.setLevel(level)

    return handler


def configure_logging(handlers: Iterable[logging.Handler], level: str = logging.DEBUG) -> None:
    """
    Configures the logging with the specified handlers and logging level.

    :param handlers: A list of logging handlers to be used for logging.
    :type handlers: Iterable[logging.Handler]

    :param level: The global logging level. Defaults to logging.DEBUG.
    :type level: str
    """

    logging.basicConfig(handlers=handlers, level=level, force=True)
