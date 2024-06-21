from colorama import Fore, Style, init

import logging


class ColorfulConsoleFormatter(logging.Formatter):
    """
    A custom logging formatter that adds colors to console log messages using colorama.

    :param fmt: The log message format string.
    :type fmt: str

    :ivar fmt: The log message format string.
    :vartype fmt: str

    :cvar COLORS: Mapping of log levels to their corresponding colors.
    :cvartype COLORS: Dict[int, str]
    """

    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT
    }

    def __init__(self, fmt: str):
        super(ColorfulConsoleFormatter, self).__init__()
        self.fmt = fmt
        init(autoreset=True)

    def format(self, record):
        color = self.COLORS.get(record.levelno, Fore.WHITE)
        formatter = logging.Formatter(fmt=color + self.fmt + Style.RESET_ALL)
        return formatter.format(record)
