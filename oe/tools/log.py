import logging
import oe.tools as tools
import oe.core.tools as core

from oe.utils.const import NAME_MAPPING


class Log(core.Log):
    @classmethod
    def _log(cls, level, name, message=None):
        actual_name = NAME_MAPPING.get(name, name)
        message = message or tools.String.wrap_text(name)
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

    @classmethod
    def installer_logger(cls):
        return logging.getLogger("Installer")

    @classmethod
    def registry_logger(cls):
        return logging.getLogger("Registry")

    @classmethod
    def fileio_logger(cls):
        return logging.getLogger("FileIO")

    @classmethod
    def maya_logger(cls):
        return logging.getLogger("Maya")

    @classmethod
    def gui_logger(cls):
        return logging.getLogger("GUI")

    @classmethod
    def packages_logger(cls):
        return logging.getLogger("Packages")

    @classmethod
    def storage_logger(cls):
        return logging.getLogger("Storage")

    # Module Logging
    @classmethod
    def set_project_logger(cls):
        return logging.getLogger("SetProject")

    @classmethod
    def parse_xml_logger(cls):
        return logging.getLogger("ParseXML")

    @classmethod
    def parse_resources_logger(cls):
        return logging.getLogger("ParseResources")

    @classmethod
    def import_resources_logger(cls):
        return logging.getLogger("ImportResources")

    @classmethod
    def write_xml_logger(cls):
        return logging.getLogger("WriteXML")
