import logging

import oe.tools as tools
import oe.core.tools as core

class Logging(core.Logging):
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
    def operator_logger(cls):
        return logging.getLogger("Operator")
