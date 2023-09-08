import os

import oe.tools as tools

from oe.utils import qt


class ParseResourcesData:
    props = {}

    dir = None
    models_paths = None
    models_paths_sorted_by_size = None
    models_paths_sorted_filenames = None
    models_paths_sorted_filesizes = None

    @classmethod
    def purse(cls):
        cls.dir = None
        cls.models_paths = None
        cls.models_paths_sorted_by_size = None
        cls.models_paths_sorted_filenames = None
        cls.models_paths_sorted_filesizes = None

    @classmethod
    def load(cls, _dir):
        cls.dir = _dir
        cls.models_paths = cls.get_models_paths()
        cls.models_paths_sorted_by_size = cls.get_models_paths_sorted_by_size()
        cls.models_paths_sorted_filenames = cls.get_models_paths_sorted_filenames()
        cls.models_paths_sorted_filesizes = cls.get_models_paths_sorted_filesizes()

    @classmethod
    def get_models_paths(cls):
        return tools.IO.list_filtered_paths(
            cls.dir, re_pattern="fbx|obj", recursive=True
        )

    @classmethod
    def get_models_paths_sorted_by_size(cls):
        return tools.IO.sort_files_by_size(
            cls.models_paths, is_reverse=True, is_dict=True
        )

    @classmethod
    def get_models_paths_sorted_filenames(cls):
        return [os.path.split(key)[1] for key in cls.models_paths_sorted_by_size.keys()]

    @classmethod
    def get_models_paths_sorted_filesizes(cls):
        return [
            tools.IO.bytes_to_readable_size(val)
            for val in cls.models_paths_sorted_by_size.values()
        ]
