import importlib
import sys
from oe.utils.logging import packages_logger

DEFAULT_RELOAD_PACKAGES = []


def reload(packages=None):
    if packages is None:
        packages_logger.info("No packages specified, using default packages")
        packages = DEFAULT_RELOAD_PACKAGES

    for mod in upload(packages=packages):
        packages_logger.info(f"Reloading module: {mod}")
        importlib.reload(mod)


def upload(packages=None):
    packages_logger.info("Constructing unload list")
    reload_list = []
    for mod in sys.modules.keys():
        for package in packages:
            if mod.startswith(package):
                reload_list.append(mod)

    packages_logger.info("Unloading modules")
    unloaded_modules = []
    for mod in reload_list:
        try:
            if sys.modules[mod] is not None:
                unloaded_modules.append(sys.modules[mod])
        except KeyError:
            packages_logger.warning(f"Module {mod} not found in sys.modules")
        except TypeError:
            packages_logger.warning(f"Invalid type for module key: {mod}")

    return unloaded_modules
