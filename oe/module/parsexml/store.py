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

    # prop_nodes
    @classmethod
    def get_prop_nodes_datasource(cls):
        return cls.props["nodes_datasource"]

    @classmethod
    def get_prop_nodes_objects(cls):
        return cls.props["nodes_objects"]

    @classmethod
    def get_prop_nodes_objects_by_type(cls):
        return cls.props["nodes_objects_by_type"]

    @classmethod
    def get_prop_nodes_objects_valid_by_type(cls):
        return cls.props["nodes_objects_valid_by_type"]

    @classmethod
    def get_prop_nodes_objects_invalid_by_type(cls):
        return cls.props["nodes_objects_invalid_by_type"]

    @classmethod
    def get_prop_nodes_objects_temporary_by_type(cls):
        return cls.props["nodes_objects_temporary_by_type"]

    @classmethod
    def get_prop_nodes_objects_duplicate_by_type(cls):
        return cls.props["nodes_objects_duplicate_by_type"]

    @classmethod
    def get_prop_nodes_objects_available_by_type(cls):
        return cls.props["nodes_objects_available_by_type"]

    # prop_data
    @classmethod
    def get_prop_data_datasource(cls):
        return cls.props["data_datasource"]

    @classmethod
    def get_prop_data_objects(cls):
        return cls.props["data_objects"]

    @classmethod
    def get_prop_data_objects_by_type(cls):
        return cls.props["data_objects_by_type"]

    @classmethod
    def get_prop_data_objects_valid_by_type(cls):
        return cls.props["data_objects_valid_by_type"]

    @classmethod
    def get_prop_data_objects_invalid_by_type(cls):
        return cls.props["data_objects_invalid_by_type"]

    @classmethod
    def get_prop_data_objects_temporary_by_type(cls):
        return cls.props["data_objects_temporary_by_type"]

    @classmethod
    def get_prop_data_objects_duplicate_by_type(cls):
        return cls.props["data_objects_duplicate_by_type"]

    @classmethod
    def get_prop_data_objects_available_by_type(cls):
        return cls.props["data_objects_available_by_type"]

    @classmethod
    def get_prop_data_objects_enum_model_by_type(cls):
        return cls.props["data_objects_enum_model_by_type"]

    @classmethod
    def get_prop_data_objects_enum_bundle_by_type(cls):
        return cls.props["data_objects_enum_bundle_by_type"]

    @classmethod
    def get_prop_data_types(cls):
        return cls.props["data_types"]


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
            raise ValueError(f"Parent group ID {parent_id} does not exist.")
        if id not in self.context[parent_id]["children"]:
            raise ValueError(f"Widget ID {id} does not exist in group {parent_id}.")
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
