import ocmseditor.oe.qt as qt
import ocmseditor.tool as tool


def refresh():
    TreeItemsData.is_loaded = False
    MayaNodesData.is_loaded = False


class TreeItemsData:
    __tree = None
    __treeitems = {}

    @classmethod
    def purse(cls):
        cls.__tree = None
        cls.__treeitems = {}

    @classmethod
    def update(cls, tree):
        cls.purse()
        cls.__tree = tree
        cls.__tree.clear()
        cls.prepare_treeitems()
        cls.construct_tree_hierarchy()

    @classmethod
    def prepare_treeitems(cls):
        ocms = tool.OCMS.get_ocms()
        for uuid in ocms.met.get_data().keys():
            item = qt.QtTreeItemCSWidget()
            item.setText(0, uuid)
            cls.__treeitems.update({uuid: item})

    @classmethod
    def construct_tree_hierarchy(cls):
        ocms = tool.OCMS.get_ocms()
        for uuid, data in ocms.met.get_data().items():
            parent_uuid = data["maya"]["parent"]
            cls.add_tree_item(uuid, parent_uuid)

    @classmethod
    def add_tree_item(cls, uuid, parent_uuid):
        if cls.is_exist(parent_uuid):
            cls.add_child_tree_element(uuid, parent_uuid)
        else:
            cls.add_top_level_tree_element(uuid)

    @classmethod
    def del_tree_item(cls, uuid, parent_uuid):
        if parent_uuid == "":
            return
        parent_item = cls.__treeitems.get(parent_uuid, None)
        if parent_item:
            parent_item.removeChild(cls.__treeitems.get(uuid, None))

    @classmethod
    def add_top_level_tree_element(cls, uuid):
        cls.__tree.addTopLevelItem(cls.get_treeitem(uuid))

    @classmethod
    def add_child_tree_element(cls, uuid, parent_uuid):
        cls.get_treeitem(parent_uuid).addChild(cls.get_treeitem(uuid))

    @classmethod
    def get_treeitem(cls, uuid):
        if not cls.is_exist(uuid):
            cls.add_treeitem(uuid)
        return cls.__treeitems[uuid]

    @classmethod
    def is_exist(cls, uuid):
        return cls.__treeitems.get(uuid, None) is not None

    @classmethod
    def add_treeitem(cls, uuid):
        item = qt.QtTreeItemCSWidget()
        item.setText(0, uuid)
        cls.__treeitems.update({uuid: item})

    @classmethod
    def expand_all(cls, expand):
        for treeitem in cls.__treeitems.values():
            treeitem.setExpanded(expand)


class MayaNodesData:
    __is_loaded = False
    __maya_nodes = {}

    @classmethod
    def purse(cls):
        __is_loaded = False
        cls.__maya_nodes = {}

    @classmethod
    def update(cls):
        cls.clean_maya_scene()
        cls.purse()
        cls.construct_maya_groups()
        # cls.construct_maya_hierarchy()
        cls.__is_loaded = True

    @classmethod
    def clean_maya_scene(cls):
        if cls.__is_loaded:
            for node in cls.__maya_nodes.values():
                if not tool.Maya.obj_exists(node):
                    continue
                tool.Maya.delete(node)

    @classmethod
    def construct_maya_groups(cls):
        ocms = tool.OCMS.get_ocms()
        for uuid, data in ocms.met.get_data().items():
            if tool.Maya.obj_exists(tool.Name.to_underscore(uuid)):
                print("Maya node already exist")
                continue
            parent_uuid = data["maya"]["parent"]
            cls.add_maya_node(uuid, parent_uuid)

            # node = tool.Maya.add_group(tool.Name.to_underscore(uuid))
            # cls.__maya_nodes.update({uuid: node})

    @classmethod
    def add_maya_node(cls, uuid, parent_uuid):
        if not cls.is_exist(uuid):
            node = tool.Maya.add_group(tool.Name.to_underscore(uuid))
            cls.__maya_nodes.update({uuid: node})
        if cls.is_exist(parent_uuid):
            cls.set_parent(uuid, parent_uuid)

        ocms = tool.OCMS.get_ocms()
        met = ocms.met
        config = met.get_config()
        conf_component = config["component"]

        data = met.get_data()[uuid]

        typ = data["object"]["type"]
        category = data["object"]["category"]
        name = data["object"]["name"]
        alias = data["object"]["alias"]
        model = data["object"]["model"]
        bundle = data["object"]["bundle"]
        time = data["object"]["time"]
        noted = data["object"]["noted"]
        remark = data["object"]["remark"]
        id = data["object"]["id"]

        compound_name = "Object"
        attrs = {
            "type": typ,
            "category": category,
            "name": name,
            "alias": alias,
            "model": model,
            "bundle": bundle,
            "time": time,
            "noted": noted,
            "remark": remark,
            "id": id,
        }
        tool.Maya.setup_string_attr_to_obj(
            compound_name, attrs, tool.Name.to_underscore(uuid)
        )

        # Component
        components = data["component"][conf_component]

        for __component in components:
            compound_name = tool.Name.to_underscore(__component["name"])
            properties = __component["property"]
            attrs = {}
            for __property in properties:
                attrs.update(
                    {
                        compound_name
                        + tool.Name.to_underscore(__property["name"]): __property[
                            "text"
                        ]
                    }
                )

            tool.Maya.setup_string_attr_to_obj(
                compound_name, attrs, tool.Name.to_underscore(uuid)
            )

    @classmethod
    def del_maya_node(cls, uuid, parent_uuid):
        if cls.is_exist(uuid):
            if parent_uuid == "":
                return
            tool.Maya.delete(tool.Name.to_underscore(uuid))
            cls.__maya_nodes.pop(uuid)

    @classmethod
    def construct_maya_hierarchy(cls):
        ocms = tool.OCMS.get_ocms()
        for uuid, data in ocms.met.get_data().items():
            parent_uuid = data["maya"]["parent"]
            cls.set_parent(uuid, parent_uuid)

    @classmethod
    def set_parent(cls, uuid, parent_uuid):
        if cls.is_exist(parent_uuid):
            tool.Maya.parent(
                tool.Name.to_underscore(uuid), tool.Name.to_underscore(parent_uuid)
            )

    @classmethod
    def is_exist(cls, uuid):
        return cls.__maya_nodes.get(uuid, None) is not None
