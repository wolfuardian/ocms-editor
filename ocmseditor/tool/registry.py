import winreg

import ocmseditor.core.tool as core
import ocmseditor.oe.data.const as const


class Registry(core.Registry):
    @classmethod
    def get_reg(cls, data_name, reserved=0, default=""):
        """
        從 Windows 註冊表中讀取特定名稱的數據。

        範例:
            data = YourClass.get("SomeKeyName")
            print(data)  # 輸出可能是 'SomeValue' 或者提供的預設值。

        參數:
            data_name: 註冊表項目的名稱。
            reserved: 保留參數，通常為 0。
            default: 如果讀取失敗，則返回的預設值。

        返回:
            讀取到的數據或預設值。
        """
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, const.REG_KEY, reserved, winreg.KEY_READ
        ) as key:
            try:
                with winreg.OpenKey(
                    key, const.REG_SUB, reserved, winreg.KEY_READ
                ) as subkey:
                    value = winreg.QueryValueEx(subkey, data_name)[0]
                    return value
            except PermissionError:
                return default
            except WindowsError:
                return default
            except (AttributeError, NameError):
                return default
            except (TypeError, ValueError):
                return default
            except Exception as e:
                return default

    @classmethod
    def set_reg(cls, data_name, data_value, reserved=0, data_type=winreg.REG_SZ):
        """
        在 Windows 註冊表中設置特定名稱的數據。

        範例:
            YourClass.set("SomeKeyName", "SomeValue")

        參數:
            data_name: 註冊表項目的名稱。
            data_value: 設置的數據值。
            reserved: 保留參數，通常為 0。
            data_type: 數據類型，預設為 winreg.REG_SZ（字符串）。

        返回:
            設置的數據值。
        """
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, const.REG_KEY, reserved, winreg.KEY_WRITE
        ) as key:
            try:
                with winreg.OpenKey(
                    key, const.REG_SUB, reserved, winreg.KEY_WRITE
                ) as subkey:
                    winreg.SetValueEx(
                        subkey, data_name, reserved, data_type, data_value
                    )
                return data_value
            except WindowsError:
                with winreg.CreateKey(key, const.REG_SUB) as subkey:
                    winreg.SetValueEx(
                        subkey, data_name, reserved, data_type, data_value
                    )
        return data_value
