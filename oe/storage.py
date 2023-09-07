import os
import oe.tools as tools

from oe.refer import Registry as reg_


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
        self.path = path
        self.is_dir = False
        self.is_file = False
        self.is_exists = False

        self.validate()

    def purse(self):
        self.path = None
        self.is_dir = False
        self.is_file = False
        self.is_exists = False

    def validate(self):
        if not self.path or self.path == "":
            self.purse()
        else:
            self.is_exists = tools.IO.is_exists(self.path)
            self.is_dir = tools.IO.is_dir(self.path)
            self.is_file = tools.IO.is_file(self.path)

    def is_valid(self):
        return self.is_exists and (self.is_dir or self.is_file)


class Registry:
    def __init__(self, name, key=reg_.REG_KEY, sub=reg_.REG_SUB):
        self._key = key
        self._sub = sub
        self._name = name
        self._value = None

        self._fetch()

    def clear(self):
        self._key = None
        self._sub = None
        self._name = None
        self._value = None

    def _fetch(self):
        self._value = tools.Registry.get_value(self._key, self._sub, self._name, "")

    def set(self, value):
        self._value = value
        tools.Registry.set_value(self._key, self._sub, self._name, self._value)
        return self._value

    def get(self):
        return self._value
