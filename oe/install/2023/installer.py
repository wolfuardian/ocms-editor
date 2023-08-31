# -*- coding: utf-8 -*-
import os
import getpass
from version import version as ver
from oe.utils.logging import installer_logger, fileio_logger
from oe.utils.registry import Registry



env_dir = f"C:/Users/{getpass.getuser()}/PycharmProjects"

mod = ver.split("-")[0] + "-" + ver.split("-")[1]
mod_ver = ver.split("-")[2]
mod_dir = f"{env_dir}/{mod}"

maya_ver = "2023"
maya_mod_dir = f"C:/Users/{getpass.getuser()}/Documents/maya/{maya_ver}/modules"
maya_mod_file = f"{maya_mod_dir}/{mod}.mod"


def install():
    if not os.path.exists(maya_mod_dir):
        fileio_logger.info(f"Creating module folder: {maya_mod_dir}")
        os.makedirs(maya_mod_dir)

    command = f"""+ {mod} {mod_ver} {mod_dir}
scripts: {mod_dir}"""

    fileio_logger.info(f"Creating module file: {maya_mod_file}")
    fp = open(maya_mod_file, "w")
    fp.write(command)
    fp.close()

    installer_logger.info(f"Saving {mod} preferences")
    Registry.set_value("Software", mod, "Pref_ModuleName", mod)
    Registry.set_value("Software", mod, "Pref_ModuleEnvDirectory", env_dir)
    Registry.set_value("Software", mod, "Pref_ModuleProjectDirectory", mod_dir)
    Registry.set_value("Software", mod, "Pref_MayaVersion", maya_ver)
    Registry.set_value("Software", mod, "Pref_MayaModuleFolder", maya_mod_dir)
    Registry.set_value("Software", mod, "Pref_MayaModuleFile", maya_mod_file)


def uninstall():
    try:
        fileio_logger.info(f"Removing module file: {maya_mod_file}")
        os.remove(maya_mod_file)

    except WindowsError:
        fileio_logger.error(f"{mod} module file does not exist.")

    installer_logger.info(f"Removing {mod} preferences")
    Registry.delete_subkey("Software", mod)


if __name__ == "__main__":
    install()
