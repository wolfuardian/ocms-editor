import os
import oe.tools as tools

from oe.utils import qt
from oe.utils import const as c


class XMLData:
    props = {}

    path = None
    xmlstring = None
    root = None

    nodes_objects = None
    nodes_datasource = None

    data_objects = None
    data_datasource = None

    tags = None
    attrs = None
    types = None

    non_device_types = None

    @classmethod
    def purse(cls):
        cls.props = {}

        cls.path = None
        cls.xmlstring = None
        cls.root = None

        cls.nodes_objects = None
        cls.nodes_datasource = None

        cls.data_objects = None
        cls.data_datasource = None

        cls.tags = None
        cls.attrs = None
        cls.types = None

        cls.non_device_types = None

    @classmethod
    def update(cls, store):
        cls.props = store.props

        cls.path = store.path
        cls.xmlstring = store.xmlstring
        cls.root = store.root

        cls.nodes_objects = store.nodes_objects
        cls.nodes_datasource = store.nodes_datasource

        cls.data_objects = store.data_objects
        cls.data_datasource = store.data_datasource

        cls.tags = store.tags
        cls.attrs = store.attrs
        cls.types = store.types

        cls.non_device_types = store.non_device_types


class ResourcesData:
    props = {}

    dir = None
    models_paths = None
    models_paths_sorted_by_size = None
    models_paths_sorted_filenames = None
    models_paths_sorted_filesizes = None

    @classmethod
    def purse(cls):
        cls.props = {}

        cls.dir = None
        cls.models_paths = None
        cls.models_paths_sorted_by_size = None
        cls.models_paths_sorted_filenames = None
        cls.models_paths_sorted_filesizes = None

    @classmethod
    def update(cls, store):
        cls.props = store.props

        cls.dir = store.dir
        cls.models_paths = store.models_paths
        cls.models_paths_sorted_by_size = store.models_paths_sorted_by_size
        cls.models_paths_sorted_filenames = store.models_paths_sorted_filenames
        cls.models_paths_sorted_filesizes = store.models_paths_sorted_filesizes


class UIData:
    ui = {}


class Path:
    def __init__(self, path):
        self.__path = path
        self.__is_dir = False
        self.__is_file = False
        self.__is_exists = False

        self.__is_xml = False

        self.validate()

    def purse(self):
        self.__path = None
        self.__is_dir = False
        self.__is_file = False
        self.__is_exists = False

        self.__is_xml = False

    def validate(self):
        if not self.__path or self.__path == "":
            self.purse()
        else:
            self.__is_exists = tools.IO.is_exists(self.__path)
            self.__is_dir = tools.IO.is_dir(self.__path)
            self.__is_file = tools.IO.is_file(self.__path)
            self.__is_xml = tools.IO.is_xml(self.__path)

    def is_valid(self):
        return self.__is_exists and (self.__is_dir or self.__is_file)

    def is_dir(self):
        return self.__is_dir

    def is_file(self):
        return self.__is_file

    def is_exists(self):
        return self.__is_exists

    def is_xml(self):
        return self.__is_xml


class Registry:
    def __init__(self, name, key=c.REG_KEY, sub=c.REG_SUB):
        self.__key = key
        self.__sub = sub
        self.__name = name
        self.__value = None

        self._fetch()

    def clear(self):
        self.__key = None
        self.__sub = None
        self.__name = None
        self.__value = None

    def _fetch(self):
        self.__value = tools.Registry.get_value(self.__key, self.__sub, self.__name, "")

    def set(self, value):
        self.__value = value
        tools.Registry.set_value(self.__key, self.__sub, self.__name, self.__value)
        return self.__value

    def get(self):
        return self.__value


class Widget:
    def __init__(self, widget):
        self.__widget = widget

    def hide(self):
        self.__widget.set_force_visible(False)

    def show(self):
        self.__widget.set_force_visible(True)

    def enable(self):
        self.__widget.setEnabled(True)

    def disable(self):
        self.__widget.setEnabled(False)

    def set_text(self, text):
        self.__widget.setText(text)
        self.__widget.setCursorPosition(0)

    def get_widget(self):
        return self.__widget


class QtGroupbox:
    def __init__(self):
        self.__groupbox = qt.QtGroupVBoxCSWidget(margin=(0, 0, 0, 0))
        self.__groupbox.set_status(qt.QtGroupBoxStatus.Border)
        self.__layout = self.__groupbox.layout
        self.__context = {}

    def get_groupbox(self):
        return self.__groupbox

    def add_group(self, id, widget):
        if id in self.__context:
            raise ValueError(f"Group ID {id} already exists.")
        self.__context[id] = {"widget": widget, "children": {}}
        self.__layout.addWidget(widget)

    def remove_group(self, id):
        if id not in self.__context:
            raise ValueError(f"Group ID {id} does not exist.")
        widget = self.__context[id]["widget"]
        widget.deleteLater()
        del self.__context[id]

    def add_widget(self, parent_id, id, widget):
        if parent_id not in self.__context:
            raise ValueError(f"Parent group ID {parent_id} does not exist.")
        if id in self.__context[parent_id]["children"]:
            raise ValueError(f"Widget ID {id} already exists in group {parent_id}.")
        self.__context[parent_id]["children"][id] = widget
        self.__context[parent_id]["widget"].__layout.addWidget(widget)

    def remove_widget(self, parent_id, id):
        if parent_id not in self.__context:
            raise ValueError(f"Parent group ID {parent_id} does not exist.")
        if id not in self.__context[parent_id]["children"]:
            raise ValueError(f"Widget ID {id} does not exist in group {parent_id}.")
        widget = self.__context[parent_id]["children"][id]
        widget.deleteLater()
        del self.__context[parent_id]["children"][id]

    def clear_group(self, group_id):
        if group_id not in self.__context:
            raise ValueError(f"Group ID {group_id} does not exist.")
        for id, widget in self.__context[group_id]["children"].items():
            widget.deleteLater()
        self.__context[group_id]["children"].clear()

    def clear_all(self):
        for group_id, group_data in self.__context.items():
            for id, widget in group_data["children"].items():
                widget.deleteLater()
            group_data["widget"].deleteLater()
        self.__context.clear()
