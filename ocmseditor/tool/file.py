import io
import re
import os
import glob
import subprocess

import ocmseditor.core.tool as core
import ocmseditor.tool as tool
import ocmseditor.oe.helper as helper
import ocmseditor.oe.data.const as const


class File(core.File):
    @classmethod
    def exists(cls, path):
        """
        檢查指定的路徑是否存在。

        範例:
            path = "/path/to/file"
            exists = YourClass.exists(path)

        參數:
            path: 要檢查的路徑字符串。

        返回:
            一個布爾值，表示路徑是否存在。
        """
        return os.path.exists(path)

    @classmethod
    def is_dir(cls, path):
        """
        判斷指定的路徑是否為目錄。

        範例:
            path = "/path/to/dir"
            is_directory = YourClass.is_dir(path)

        參數:
            path: 要檢查的路徑字符串。

        返回:
            一個布爾值，表示路徑是否為目錄。
        """
        return os.path.isdir(path)

    @classmethod
    def is_file(cls, path):
        """
        判斷指定的路徑是否為文件。

        範例:
            path = "/path/to/file"
            is_file = YourClass.is_file(path)

        參數:
            path: 要檢查的路徑字符串。

        返回:
            一個布爾值，表示路徑是否為文件。
        """
        return os.path.isfile(path)

    @classmethod
    def is_xml(cls, path):
        """
        判斷指定的路徑是否為 XML 文件。

        範例:
            path = "/path/to/file.xml"
            is_xml_file = YourClass.is_xml(path)

        參數:
            path: 要檢查的路徑字符串。

        返回:
            一個布爾值，表示路徑是否為 XML 文件。
        """
        return path.endswith(".xml")

    @classmethod
    def glob(cls, directory, extension=None, pattern=None, recursive=False):
        """
        搜尋指定目錄下符合特定條件的文件或目錄，並返回其路徑列表。

        範例:
            paths = YourClass.glob("/path/to/directory", extension=".txt")
            paths_with_pattern = YourClass.glob("/path/to/directory", pattern="txt|csv")

        參數:
            directory: 要搜尋的目錄路徑。
            extension: 文件擴展名過濾條件，例如“.txt”。
            pattern: 正則表達式模式用於進一步過濾搜尋結果。
            recursive: 是否遞迴搜尋子目錄。

        返回:
            一個包含符合條件的文件或目錄路徑的列表。
        """

        search_pattern = os.path.join(directory, "**", f"*{extension or ''}")
        paths = glob.glob(search_pattern, recursive=recursive)
        paths = [path.replace("\\", "/") for path in paths]

        if pattern:
            compiled_pattern = re.compile(rf".*\.({pattern})$", re.IGNORECASE)
            paths = [path for path in paths if compiled_pattern.findall(path)]
            paths = [path.replace("\\", "/") for path in paths]

        return paths

    @classmethod
    def read_utf16(cls, path):
        """
        嘗試讀取位於指定路徑的UTF-16編碼文本文件。

        範例:
            path = "/path/to/utf16file.txt"
            content = YourClass.read_utf16(path)

        參數:
            path: 需要讀取的UTF-16編碼文件的路徑。

        返回:
            如果成功，返回一個包含文件內容的字符串。
            如果文件不存在或不是有效的UTF-16編碼文本，則返回None。
        """
        try:
            with io.open(path, mode="r", encoding="utf-16") as file:
                content = file.read()
            return content
        except FileNotFoundError:
            helper.Logger.warning(__name__, f"File {path} not found.")
            return None
        except UnicodeDecodeError:
            helper.Logger.warning(
                __name__, f"File {path} is not a valid UTF-16 encoded text."
            )
            return None

    @classmethod
    def get_size(cls, path):
        """
        獲取指定文件的大小（以字節為單位）。

        範例:
            file_size = YourClass.get_size("/path/to/file.txt")

        參數:
            path: 要獲取大小的文件的路徑。

        返回:
            指定文件的大小（以字節為單位），或在出現錯誤時返回 None。
        """
        if not path:
            helper.Logger.warning(__name__, "Path is empty.")
            return None
        try:
            return os.path.getsize(path)
        except FileNotFoundError as e:
            helper.Logger.warning(__name__, f"File not found: {e}")
            return None

    @classmethod
    def get_project_path(cls):
        """
        從註冊表中獲取專案路徑。

        範例:
            YourClass.get_project_path()  # 從註冊表中返回專案路徑

        返回:
            註冊表中存儲的專案路徑。
        """
        return tool.Registry.get_reg(const.REG_PROJ_PATH)

    @classmethod
    def get_copy_to_path(cls, path):
        """
        生成從源文件路徑拷貝到目標工程路徑的絕對路徑。

        範例:
            target_path = YourClass.get_copy_to_path("/source/path/to/file.ext")
            # 輸出可能是："project_path/model_name/file.fbx"

        參數:
            path: 源文件的絕對或相對路徑。

        返回:
            目標工程路徑的絕對路徑，包括目標文件名。
        """
        if not path:
            helper.Logger.warning(__name__, "Path is empty.")
            return ""
        project_path = tool.File.get_project_path()
        model_name = tool.File.split_basename_without_ext(path).lower()
        filename = model_name + ".fbx"
        return os.path.join(project_path, model_name, filename).replace("\\", "/")

    @classmethod
    def bytes_to_readable_size(cls, size_bytes, precision=2, unit=None):
        """
        將字節數轉換為易讀的文件大小。

        範例:
            readable_size = YourClass.bytes_to_readable_size(1024)  # 輸出："1.00 KB"

        參數:
            size_bytes: 文件大小，以字節為單位。
            precision: 輸出的小數點精度（預設為 2）。
            unit: 可選，一個包含各種單位（如 "B", "KB", "MB" 等）的列表。

        返回:
            文件大小的易讀表示，包括單位。
        """
        if unit is None:
            unit = const.SIZE_UNITS
        i = 0
        while size_bytes >= 1024 and i < len(unit) - 1:
            size_bytes /= 1024
            i += 1
        return f"{size_bytes:.{precision}f} {unit[i]}"

    @classmethod
    def split_basename_without_ext(cls, path):
        """
        獲取不包括擴展名的基本文件名。

        範例:
            YourClass.split_basename_without_ext("C:/path/to/file.txt")  # 返回 'file'

        參數:
            path: 文件的絕對或相對路徑。

        返回:
            不包括擴展名的基本文件名。
        """
        return os.path.splitext(os.path.basename(path))[0]

    @classmethod
    def open_on_explorer(cls, path):
        """
        打開 Windows 資源管理器並選中指定的文件或文件夾。

        範例:
            YourClass.open_on_explorer("C:/path/to/file_or_folder")

        參數:
            path: 指定的文件或文件夾的絕對路徑。

        異常:
            ValueError: 如果指定的路徑不存在。
        """
        helper.Logger.info(__name__, f"Opening {path} on explorer")
        if not os.path.exists(path):
            raise ValueError(f"{path} does not exist.")

        path = path.replace("/", "\\")
        command = f'explorer /select,"{path}"'
        subprocess.Popen(command, shell=True)
