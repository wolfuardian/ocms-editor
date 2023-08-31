import winreg
import warnings


class Registry:
    @classmethod
    def create_key(cls, key_name, subkey_name):
        pass

    @classmethod
    def set_value(cls, key_name, subkey_name, val_name, val_data, val_type=winreg.REG_SZ):
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_name, 0, winreg.KEY_WRITE) as key:
            try:
                with winreg.OpenKey(key, subkey_name, 0, winreg.KEY_WRITE) as subkey:
                    winreg.SetValueEx(subkey, val_name, 0, val_type, val_data)
            except WindowsError:
                with winreg.CreateKey(key, subkey_name) as subkey:
                    winreg.SetValueEx(subkey, val_name, 0, val_type, val_data)

    @classmethod
    def get_value(cls, key_name, subkey_name, value_name, default=""):
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_name, 0, winreg.KEY_READ) as key:
            try:
                with winreg.OpenKey(key, subkey_name, 0, winreg.KEY_READ) as subkey:
                    value = winreg.QueryValueEx(subkey, value_name)[0]
                    return value
            except WindowsError:
                return default

    @classmethod
    def create_subkey(cls, key_name, subkey_name):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_name, 0, winreg.KEY_ALL_ACCESS)
        subkey = winreg.CreateKey(key, subkey_name)
        winreg.CloseKey(key)
        return subkey

    @classmethod
    def delete_subkey(cls, key_name, subkey_name):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_name, 0, winreg.KEY_ALL_ACCESS)
            winreg.DeleteKey(key, subkey_name)
            winreg.CloseKey(key)

        except WindowsError:
            warnings.warn(f"Subkey '{subkey_name}' does not exist in key '{key_name}'.")
