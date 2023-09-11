import winreg

import ocmseditor.core.tool as core

from ocmseditor import tool


class Registry(core.Registry):
    @classmethod
    def create_key(cls, key_name, subkey_name):
        tool.Log.info(__name__, f"Creating subkey '{subkey_name}' in key '{key_name}'")
        pass

    @classmethod
    def set_value(
        cls, key_name, subkey_name, val_name, val_data, val_type=winreg.REG_SZ
    ):
        tool.Log.info(
            __name__,
            f"Setting value '{val_name}' to '{val_data}' in subkey '{subkey_name}' of key '{key_name}'",
        )
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, key_name, 0, winreg.KEY_WRITE
        ) as key:
            try:
                with winreg.OpenKey(key, subkey_name, 0, winreg.KEY_WRITE) as subkey:
                    winreg.SetValueEx(subkey, val_name, 0, val_type, val_data)
                return val_data
            except WindowsError:
                with winreg.CreateKey(key, subkey_name) as subkey:
                    winreg.SetValueEx(subkey, val_name, 0, val_type, val_data)

    @classmethod
    def get_value(cls, key_name, subkey_name, value_name, default=""):
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, key_name, 0, winreg.KEY_READ
        ) as key:
            try:
                with winreg.OpenKey(key, subkey_name, 0, winreg.KEY_READ) as subkey:
                    value = winreg.QueryValueEx(subkey, value_name)[0]
                    return value
            except PermissionError:
                tool.Log.error(
                    __name__, "Permission denied: Unable to access the registry."
                )
                return default
            except WindowsError:
                tool.Log.warning(
                    __name__,
                    f"Subkey '{subkey_name}' does not exist in key '{key_name}'.",
                )
                return default
            except (AttributeError, NameError):
                tool.Log.error(__name__, f"Function or module not found.")
                return default

            except (TypeError, ValueError):
                tool.Log.error(__name__, f"Invalid argument provided.")
                return default

            except Exception as e:
                tool.Log.error(__name__, f"An unexpected error occurred: {e}")
                return default

    @classmethod
    def create_subkey(cls, key_name, subkey_name):
        tool.Log.info(__name__, f"Creating subkey '{subkey_name}' in key '{key_name}'")
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, key_name, 0, winreg.KEY_ALL_ACCESS
        )
        subkey = winreg.CreateKey(key, subkey_name)
        winreg.CloseKey(key)
        return subkey

    @classmethod
    def delete_subkey(cls, key_name, subkey_name):
        try:
            tool.Log.info(
                __name__, f"Removing subkey '{subkey_name}' from key '{key_name}'"
            )
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, key_name, 0, winreg.KEY_ALL_ACCESS
            )
            winreg.DeleteKey(key, subkey_name)
            winreg.CloseKey(key)

        except WindowsError:
            tool.Log.warning(
                __name__, f"Subkey '{subkey_name}' does not exist in key '{key_name}'."
            )
