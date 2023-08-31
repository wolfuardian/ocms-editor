import sys
import importlib

import oe.tools as tools
import oe.core.tools as core

DEFAULT_RELOAD_PACKAGES = []


class Packages(core.Packages):
    @classmethod
    def reload(cls, packages=None):
        if packages is None:
            tools.Logging.packages_logger().info(
                "No packages specified, using default packages"
            )
            packages = DEFAULT_RELOAD_PACKAGES

        for mod in cls.upload(packages=packages):
            tools.Logging.packages_logger().info(f"Reloading module: {mod}")
            importlib.reload(mod)

    @classmethod
    def upload(cls, packages=None):
        tools.Logging.packages_logger().info("Constructing unload list")
        reload_list = []
        for mod in sys.modules.keys():
            for package in packages:
                if mod.startswith(package):
                    reload_list.append(mod)

        tools.Logging.packages_logger().info("Unloading modules")
        unloaded_modules = []
        for mod in reload_list:
            try:
                if sys.modules[mod] is not None:
                    unloaded_modules.append(sys.modules[mod])
            except KeyError:
                tools.Logging.packages_logger().warning(
                    f"Module {mod} not found in sys.modules"
                )
            except TypeError:
                tools.Logging.packages_logger().warning(
                    f"Invalid type for module key: {mod}"
                )

        return unloaded_modules
