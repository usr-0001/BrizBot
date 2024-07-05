from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import json
import os

from pathlib import Path
from typing import AnyStr

from pydantic import ValidationError

import logging
from source.settings.models import Settings


_logger = logging.getLogger(__name__)
__all__ = ["load_settings"]


def load_settings(full_file_name: os.PathLike[AnyStr]) -> Settings:
    """
    Loads settings from a JSON file.

    :param full_file_name: The path to the JSON file containing settings.
    :type full_file_name: os.PathLike

    :return: The loaded settings.
    :rtype: Settings

    :raises FileNotFoundError: If the specified file does not exist.
    :raises ValueError: If the content of the specified file is not a dictionary.
    :raises ValidationError: If the settings can't be validated.
    """

    path = Path(full_file_name).resolve()

    if not path.is_file():
        raise FileNotFoundError(f"The file intended to be used as settings was not found at {path}")

    with open(path, "r", encoding="utf-8") as file:
        dictionary = json.load(file)

        if not isinstance(dictionary, dict):
            raise ValueError("The settings content is not a dictionary")

    try:
        settings = Settings(**dictionary)
    except ValidationError as e:
        _logger.error(f"Settings can't be validated because of the following errors: {e.errors()}")
        raise

    return settings
