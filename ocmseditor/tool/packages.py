import sys
import importlib

import ocmseditor.core.tool as core

from ocmseditor import tool

DEFAULT_RELOAD_PACKAGES = []


class Packages(core.Packages):
    @classmethod
    def reload(cls, packages=None):
        if packages is None:
            tool.Log.info(__name__, f"No packages specified, using default packages")
            packages = DEFAULT_RELOAD_PACKAGES

        for mod in cls.upload(packages=packages):
            tool.Log.info(__name__, f"Reloading module: {mod}")
            importlib.reload(mod)
        tool.Log.info(__name__, f"Completed reloading modules")

    @classmethod
    def upload(cls, packages=None):
        tool.Log.info(__name__, "Constructing unload list")
        reload_list = []
        for mod in sys.modules.keys():
            for package in packages:
                if mod.startswith(package):
                    reload_list.append(mod)

        tool.Log.info(__name__, "Unloading modules")
        unloaded_modules = []
        for mod in reload_list:
            try:
                if sys.modules[mod] is not None:
                    unloaded_modules.append(sys.modules[mod])
            except KeyError:
                tool.Log.warning(__name__, f"Module {mod} not found in sys.modules")
            except TypeError:
                tool.Log.warning(__name__, f"Invalid type for module key: {mod}")
        tool.Log.info(__name__, "Completed unloading modules")
        return unloaded_modules
