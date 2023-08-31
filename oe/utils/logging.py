import logging


class UEStyleFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[0;36m",  # Cyan
        "INFO": "\033[0;37m",  # White
        "WARNING": "\033[1;33m",  # Yellow
        "ERROR": "\033[1;31m",  # Red
        "CRITICAL": "\033[1;41m",  # Red bg
    }

    def format(self, record):
        return f"Log{record.name}: {self.COLORS.get(record.levelname)}: {record.getMessage()}\033[0m"


handler = logging.StreamHandler()
formatter = UEStyleFormatter()
handler.setFormatter(formatter)

installer_logger = logging.getLogger("Installer")
installer_logger.addHandler(handler)
installer_logger.setLevel(logging.INFO)

registry_logger = logging.getLogger("Registry")
registry_logger.addHandler(handler)
registry_logger.setLevel(logging.INFO)

fileio_logger = logging.getLogger("FileIO")
fileio_logger.addHandler(handler)
fileio_logger.setLevel(logging.INFO)

maya_logger = logging.getLogger("Maya")
maya_logger.addHandler(handler)
maya_logger.setLevel(logging.INFO)