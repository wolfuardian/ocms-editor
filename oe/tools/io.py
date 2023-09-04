from typing import List, Tuple, Union, Dict, Optional, Any
import io
import re
import os
import glob
import subprocess

import oe.tools as tools
import oe.core.tools as core

from oe.refer import IO as io_


class IO(core.IO):
    @classmethod
    def read_utf16(cls, path: str) -> Union[str, Any]:
        try:
            with io.open(path, mode="r", encoding="utf-16") as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print(f"File {path} not found.")
            return None
        except UnicodeDecodeError:
            print(f"File {path} is not a valid UTF-16 encoded text.")
            return None

    @classmethod
    def convert_to_unix_path(cls, path: str) -> str:
        return path.replace("\\", "/")

    @classmethod
    def convert_paths_to_unix_style(cls, paths: List[str]) -> List[str]:
        return [cls.convert_to_unix_path(path) for path in paths]

    @classmethod
    def list_filtered_paths(
        cls,
        directory: str,
        extension: str = ".*",
        re_pattern: str = "",
        recursive: bool = False,
    ) -> List[str]:
        search_pattern = f"{directory}/**/*{extension}"
        paths = glob.glob(search_pattern, recursive=recursive)

        if not re_pattern:
            re_pattern = ".*"
        compiled_pattern = re.compile(rf".*\.({re_pattern})$", re.IGNORECASE)

        return cls.convert_paths_to_unix_style(
            [path for path in paths if compiled_pattern.findall(path)]
        )

    @classmethod
    def sort_files_by_size(
        cls, paths: Optional[List[str]], is_reverse: bool = False, is_dict: bool = False
    ) -> Union[List[str], Dict[str, int], None]:
        if not paths:
            return {} if is_dict else []

        try:
            size_dict = {path: os.path.getsize(path) for path in paths}
        except FileNotFoundError as e:
            print(f"File not found: {e}")
            return None

        sorted_dict = dict(
            sorted(size_dict.items(), key=lambda item: item[1], reverse=is_reverse)
        )

        return sorted_dict if is_dict else list(sorted_dict.keys())

    @classmethod
    def bytes_to_readable_size(
        cls,
        size_bytes: float,
        precision: int = 2,
        size_units: Optional[List[str]] = None,
    ) -> str:
        if size_units is None:
            size_units = io_.SIZE_UNITS
        i = 0
        while size_bytes >= 1024 and i < len(size_units) - 1:
            size_bytes /= 1024
            i += 1
        return f"{size_bytes:.{precision}f} {size_units[i]}"

    @classmethod
    def browser_explorer(cls, path):
        if not os.path.exists(path):
            raise ValueError(f"{path} does not exist.")

        path = path.replace("/", "\\")
        command = f'explorer /root,"{path}"'
        subprocess.Popen(command, shell=True)