import logging
import oe.tools as tools
import oe.core.tools as core

from oe.utils.const import NAME_MAPPING

class Log(core.Log):
    @classmethod
    def logger(cls, name):
        actual_name = NAME_MAPPING.get(name, name)
        logger = logging.getLogger(actual_name)
        return logger

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
