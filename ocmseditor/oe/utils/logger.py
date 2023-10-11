import logging

from ocmseditor.oe.constant import NAME_MAPPING


class Logger:
    @classmethod
    def log(cls, level, name, message=None):
        actual_name = NAME_MAPPING.get(name, name)
        message = message or f"<{name}>"
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
        cls.log("debug", name, message)

    @classmethod
    def info(cls, name, message=None):
        cls.log("info", name, message)

    @classmethod
    def warning(cls, name, message=None):
        cls.log("warning", name, message)

    @classmethod
    def error(cls, name, message=None):
        cls.log("error", name, message)
