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


class DynamicUIGroupManager:
    def __init__(self):
        self.groupbox = qt.QtGroupVBoxCSWidget(margin=(0, 0, 0, 0))
        self.groupbox.set_status(qt.QtGroupBoxStatus.Border)
        self.layout = self.groupbox.layout
        self.context = {}

    def add_group(self, id, widget):
        if id in self.context:
            raise ValueError(f"Group ID {id} already exists.")
        self.context[id] = {"widget": widget, "children": {}}
        self.layout.addWidget(widget)

    def remove_group(self, id):
        if id not in self.context:
            raise ValueError(f"Group ID {id} does not exist.")
        widget = self.context[id]["widget"]
        widget.deleteLater()
        del self.context[id]

    def add_widget(self, parent_id, id, widget):
        if parent_id not in self.context:
            raise ValueError(f"Parent group ID {parent_id} does not exist.")
        if id in self.context[parent_id]["children"]:
            raise ValueError(f"Widget ID {id} already exists in group {parent_id}.")
        self.context[parent_id]["children"][id] = widget
        self.context[parent_id]["widget"].layout.addWidget(widget)

    def remove_widget(self, parent_id, id):
        if parent_id not in self.context:
            # raise ValueError(f"Parent group ID {parent_id} does not exist.")
            tools.Log.gui_logger().warning(
                f"Widget ID {id} does not exist in group {parent_id}."
            )
            return
        if id not in self.context[parent_id]["children"]:
            tools.Log.gui_logger().warning(
                f"Widget ID {id} does not exist in group {parent_id}."
            )
            return
            # raise ValueError(f"Widget ID {id} does not exist in group {parent_id}.")
        widget = self.context[parent_id]["children"][id]
        widget.deleteLater()
        del self.context[parent_id]["children"][id]

    def clear_group(self, group_id):
        if group_id not in self.context:
            raise ValueError(f"Group ID {group_id} does not exist.")
        for id, widget in self.context[group_id]["children"].items():
            widget.deleteLater()
        self.context[group_id]["children"].clear()

    def clear_all(self):
        for group_id, group_data in self.context.items():
            for id, widget in group_data["children"].items():
                widget.deleteLater()
            group_data["widget"].deleteLater()
        self.context.clear()
