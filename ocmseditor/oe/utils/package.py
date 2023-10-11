import sys
import importlib

from ocmseditor.oe.utils.logger import Logger

DEFAULT_RELOAD_PACKAGES = []


class PackageReloader:
    @classmethod
    def reload(cls, packages=None):
        if packages is None:
            Logger.info(
                __name__, f"No packages specified, using default packages"
            )
            packages = DEFAULT_RELOAD_PACKAGES

        for mod in cls.unload(packages=packages):
            Logger.info(__name__, f"Reloading module: {mod}")
            importlib.reload(mod)
        Logger.info(__name__, f"Completed reloading modules")

    @classmethod
    def unload(cls, packages=None):
        Logger.info(__name__, "Constructing unload list")
        reload_list = []
        for mod in sys.modules.keys():
            for package in packages:
                if mod.startswith(package):
                    reload_list.append(mod)

        Logger.info(__name__, "Unloading modules")
        unloaded_modules = []
        for mod in reload_list:
            try:
                if sys.modules[mod] is not None:
                    unloaded_modules.append(sys.modules[mod])
            except KeyError:
                Logger.warning(
                    __name__, f"Module {mod} not found in sys.modules"
                )
            except TypeError:
                Logger.warning(__name__, f"Invalid type for module key: {mod}")
        Logger.info(__name__, "Completed unloading modules")
        return unloaded_modules
