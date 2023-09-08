import sys
import importlib

import oe.tools as tools
import oe.core.tools as core

DEFAULT_RELOAD_PACKAGES = []


class Packages(core.Packages):
    @classmethod
    def reload(cls, packages=None):
        if packages is None:
            tools.Log.info(__name__, f"No packages specified, using default packages")
            packages = DEFAULT_RELOAD_PACKAGES

        for mod in cls.upload(packages=packages):
            tools.Log.info(__name__, f"Reloading module: {mod}")
            importlib.reload(mod)
        tools.Log.info(__name__, f"Completed reloading modules")

    @classmethod
    def upload(cls, packages=None):
        tools.Log.info(__name__, "Constructing unload list")
        reload_list = []
        for mod in sys.modules.keys():
            for package in packages:
                if mod.startswith(package):
                    reload_list.append(mod)

        tools.Log.info(__name__, "Unloading modules")
        unloaded_modules = []
        for mod in reload_list:
            try:
                if sys.modules[mod] is not None:
                    unloaded_modules.append(sys.modules[mod])
            except KeyError:
                tools.Log.warning(__name__, f"Module {mod} not found in sys.modules")
            except TypeError:
                tools.Log.warning(__name__, f"Invalid type for module key: {mod}")
        tools.Log.info(__name__, "Completed unloading modules")
        return unloaded_modules
