import oe.tools as tools

from oe.utils import qt


class ParseXMLData:
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
    def load(cls, path):
        cls.path = path
        cls.xmlstring = cls.get_xmlstring()
        cls.root = cls.get_root()

        cls.nodes_objects = cls.get_nodes_objects()
        cls.nodes_datasource = cls.get_nodes_datasource()

        cls.data_objects = cls.get_data_objects()
        cls.data_datasource = cls.get_data_datasource()

        cls.tags = cls.get_tags()
        cls.attrs = cls.get_attrs()
        cls.types = cls.get_types()

        cls.non_device_types = cls.get_non_device_types()

    @classmethod
    def get_xmlstring(cls):
        return tools.IO.read_utf16(cls.path)

    @classmethod
    def get_root(cls):
        return tools.XML.root(cls.xmlstring)

    @classmethod
    def get_nodes_objects(cls):
        return tools.XML.iterator(cls.root, tag="Object")

    @classmethod
    def get_nodes_datasource(cls):
        return tools.XML.iterator(cls.root, tag="DataSource")

    @classmethod
    def get_data_objects(cls):
        return tools.XML.enumerator(cls.nodes_objects, attr="name", mode=1)

    @classmethod
    def get_data_datasource(cls):
        return tools.XML.enumerator(cls.nodes_datasource, attr="ProductType")[0]

    @classmethod
    def get_tags(cls):
        return tools.XML.collect_attrs(cls.root, "tag")

    @classmethod
    def get_attrs(cls):
        return tools.XML.collect_unique_attrs(cls.root)

    @classmethod
    def get_types(cls):
        return tools.XML.enumerator(
            tools.XML.iterator(cls.root, tag="Object"), attr="type"
        )

    @classmethod
    def get_non_device_types(cls):
        if cls.data_datasource == "OCMS":
            return ["Floor", "Facility"]
        elif cls.data_datasource == "OCMS2_0":
            return ["Floor", "Room", "Unknown"]
