import logging

import ocmseditor.core.tool as core

from ocmseditor import tool
from ocmseditor.oe.data import const as c


class Log(core.Log):
    @classmethod
    def _log(cls, level, name, message=None):
        actual_name = c.NAME_MAPPING.get(name, name)
        message = message or tool.String.wrap_text(name)
        logger = logging.getLogger(actual_name)
        if level == "debug":
            logger.debug(message)
        elif level == "info":
            logger.info(message)
        elif level == "warning":
            logger.warning(message)
        elif level == "error":
            logger.error(message)
        else:
            pass

    @classmethod
    def debug(cls, name, message=None):
        cls._log("debug", name, message)

    @classmethod
    def info(cls, name, message=None):
        cls._log("info", name, message)

    @classmethod
    def warning(cls, name, message=None):
        cls._log("warning", name, message)

    @classmethod
    def error(cls, name, message=None):
        cls._log("error", name, message)
