# -*- coding: utf-8 -*-
import os
import getpass
import maya.mel as mel
import maya.cmds as cmds

from version import version as ver
from oe.utils.logging import installer_logger, fileio_logger, maya_logger
from oe.utils.registry import Registry

env_dir = f"C:/Users/{getpass.getuser()}/PycharmProjects"

mod = ver.split("-")[0] + "-" + ver.split("-")[1]
mod_ver = ver.split("-")[2]
mod_dir = f"{env_dir}/{mod}"

maya_ver = "2023"
maya_mod_dir = f"C:/Users/{getpass.getuser()}/Documents/maya/{maya_ver}/modules"
maya_mod_file = f"{maya_mod_dir}/{mod}.mod"

def uninstall():
    try:
        fileio_logger.info(f"Removing module file: {maya_mod_file}")
        os.remove(maya_mod_file)

    except WindowsError:
        fileio_logger.error(f"{mod} module file does not exist.")

    installer_logger.info(f"Removing {mod} preferences")
    Registry.delete_subkey("Software", mod)

    maya_logger.info(f"Removing {mod} shelf tab and button")
    shelf_buttons = cmds.shelfLayout(mod, query=True, childArray=True)
    if shelf_buttons:
        for button in shelf_buttons:
            cmds.deleteUI(button, control=True)
    if cmds.layout(mod, exists=True):
        cmds.deleteUI(mod, layout=True)


if __name__ == "__main__":
    uninstall()
