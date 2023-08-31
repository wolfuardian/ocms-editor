# -*- coding: utf-8 -*-
import os
import winreg
import getpass
import logging
import maya.mel as mel
import maya.cmds as cmds

# from version import version as ver
ver = "ocms-editor-2308-0024"

maya_logger = logging.getLogger("Maya")
fileio_logger = logging.getLogger("FileIO")
registry_logger = logging.getLogger("Registry")
packages_logger = logging.getLogger("Packages")
installer_logger = logging.getLogger("Installer")


env_dir = f"C:/Users/{getpass.getuser()}/PycharmProjects"

mod = ver.split("-")[0] + "-" + ver.split("-")[1]
mod_ver = ver.split("-")[2]
mod_dir = f"{env_dir}/{mod}"

maya_ver = "2023"
maya_shelf = mod.replace("-", "_")
maya_mod_dir = f"C:/Users/{getpass.getuser()}/Documents/maya/{maya_ver}/modules"
maya_mod_file = f"{maya_mod_dir}/{mod}.mod"


class Registry:
    @classmethod
    def create_key(cls, key_name, subkey_name):
        registry_logger.info(f"Creating subkey '{subkey_name}' in key '{key_name}'")
        pass

    @classmethod
    def set_value(
        cls, key_name, subkey_name, val_name, val_data, val_type=winreg.REG_SZ
    ):
        registry_logger.info(
            f"Setting value '{val_name}' to '{val_data}' in subkey '{subkey_name}' of key '{key_name}'"
        )
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, key_name, 0, winreg.KEY_WRITE
        ) as key:
            try:
                with winreg.OpenKey(key, subkey_name, 0, winreg.KEY_WRITE) as subkey:
                    winreg.SetValueEx(subkey, val_name, 0, val_type, val_data)
            except WindowsError:
                with winreg.CreateKey(key, subkey_name) as subkey:
                    winreg.SetValueEx(subkey, val_name, 0, val_type, val_data)

    @classmethod
    def get_value(cls, key_name, subkey_name, value_name, default=""):
        registry_logger.info(
            f"Getting value '{value_name}' from subkey '{subkey_name}' in key '{key_name}'"
        )
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, key_name, 0, winreg.KEY_READ
        ) as key:
            try:
                with winreg.OpenKey(key, subkey_name, 0, winreg.KEY_READ) as subkey:
                    value = winreg.QueryValueEx(subkey, value_name)[0]
                    return value
            except WindowsError:
                registry_logger.warning(
                    f"Subkey '{subkey_name}' does not exist in key '{key_name}'."
                )
                return default

    @classmethod
    def create_subkey(cls, key_name, subkey_name):
        registry_logger.info(f"Creating subkey '{subkey_name}' in key '{key_name}'")
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, key_name, 0, winreg.KEY_ALL_ACCESS
        )
        subkey = winreg.CreateKey(key, subkey_name)
        winreg.CloseKey(key)
        return subkey

    @classmethod
    def delete_subkey(cls, key_name, subkey_name):
        try:
            registry_logger.info(
                f"Removing subkey '{subkey_name}' from key '{key_name}'"
            )
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, key_name, 0, winreg.KEY_ALL_ACCESS
            )
            winreg.DeleteKey(key, subkey_name)
            winreg.CloseKey(key)

        except WindowsError:
            registry_logger.warning(
                f"Subkey '{subkey_name}' does not exist in key '{key_name}'."
            )


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

    if not cmds.layout(maya_shelf, exists=True):
        maya_logger.info(f"Creating {maya_shelf} shelf tab")
        c = 'addNewShelfTab("' + maya_shelf + '");'
        mel.eval(c)

    command = """from oe import gui
gui.show()"""

    icon_path = "/execute.png"

    shelf_mbim = cmds.shelfLayout(maya_shelf, query=True, childArray=True)
    if shelf_mbim:
        maya_logger.info(f"Clearing {maya_shelf} shelf buttons")
        for button in shelf_mbim:
            cmds.deleteUI(button, control=True)

    maya_logger.info(f"Creating {maya_shelf} shelf button")
    cmds.shelfButton(
        annotation="Run",
        image1=icon_path,
        command=command,
        parent=maya_shelf,
        label="run",
    )


if __name__ == "__main__":
    install()
