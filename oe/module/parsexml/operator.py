import oe.tools as tools

from oe.utils import qt
from oe.refer import Registry as reg_

from . import store, prop


def op_initialize_xml_path(self):
    tools.Logging.parse_xml_logger().info("Initializing xml path")

    _default_path = tools.Registry.get_value(
        reg_.REG_KEY, reg_.REG_SUB, reg_.REG_XML_PATH, ""
    )
    if _default_path == "":
        _browser_path = tools.Maya.browser(1, _default_path)
        if _browser_path == "":
            tools.Logging.parse_xml_logger().warning(
                "User canceled the browser dialog."
            )
            return
        _target_dir = tools.Registry.set_value(
            reg_.REG_KEY,
            reg_.REG_SUB,
            reg_.REG_XML_PATH,
            tools.Maya.browser(1, _default_path),
        )
        self.txt_xml_path.lineedit.setText(_target_dir)
    else:
        self.txt_xml_path.lineedit.setText(_default_path)
    self.btn_initialize.set_force_visible(False)
    self.txt_xml_path.set_force_visible(True)
    self.txt_xml_path.lineedit.setCursorPosition(0)
    self.btn_browser.set_force_visible(True)

    parse_xml(self)


def op_browser_xml_path(self):
    tools.Logging.parse_xml_logger().info("Browsing xml path")

    _default_path = tools.Registry.get_value(
        reg_.REG_KEY, reg_.REG_SUB, reg_.REG_XML_PATH, ""
    )
    _browser_path = tools.Maya.browser(1, _default_path)
    if _browser_path == "":
        tools.Logging.parse_xml_logger().warning("User canceled the browser dialog.")
        return
    _target_dir = tools.Registry.set_value(
        reg_.REG_KEY,
        reg_.REG_SUB,
        reg_.REG_XML_PATH,
        _browser_path,
    )
    self.txt_xml_path.lineedit.setText(_target_dir)
    self.txt_xml_path.lineedit.setCursorPosition(0)

    parse_xml(self)


def parse_xml(self):
    tools.Logging.gui_logger().info("Initializing dynamic ui group manager")
    self.dynamic_box.clear_all()

    tools.Logging.parse_xml_logger().info("Initializing parse xml data")
    self.parse = store.ParseXMLData()

    _path = tools.Registry.get_value(reg_.REG_KEY, reg_.REG_SUB, reg_.REG_XML_PATH, "")

    tools.Logging.parse_xml_logger().info("Loading xml data")
    self.parse.load(_path)

    tools.Logging.parse_xml_logger().info("Starting constructing variables")
    nodes_objects = self.parse.nodes_objects
    nodes_datasource = self.parse.nodes_datasource
    nodes_objects_by_type = {}
    nodes_objects_valid_by_type = {}
    nodes_objects_invalid_by_type = {}
    nodes_objects_temporary_by_type = {}
    nodes_objects_duplicate_by_type = {}
    nodes_objects_available_by_type = {}

    data_objects = self.parse.data_objects
    data_datasource = self.parse.data_datasource
    data_objects_by_type = {}
    data_objects_valid_by_type = {}
    data_objects_invalid_by_type = {}
    data_objects_temporary_by_type = {}
    data_objects_duplicate_by_type = {}
    data_objects_available_by_type = {}

    data_objects_enum_model_by_type = {}
    data_objects_enum_bundle_by_type = {}

    data_types = self.parse.types

    non_device_types = self.parse.non_device_types

    for typ in data_types:
        tools.Logging.parse_xml_logger().info("Constructing variables for type: " + typ)
        typ = typ.__str__()
        nodes_objects_by_type[typ] = tools.XML.iterator(
            self.parse.root, tag="Object", attr="type", kwd=typ
        )
        data_objects_by_type[typ] = tools.XML.enumerator(
            nodes_objects_by_type[typ], attr="name", mode=1
        )
        if typ not in non_device_types:
            if data_datasource == "OCMS":
                data_objects_enum_bundle_by_type[typ] = tools.XML.enumerator(
                    nodes_objects_by_type[typ], attr="bundle"
                )
                data_objects_enum_model_by_type[typ] = tools.XML.enumerator(
                    nodes_objects_by_type[typ], attr="model"
                )

                nodes_objects_valid_by_type[typ] = tools.XML.extractor(
                    nodes_objects_by_type[typ],
                    pos_attrs=["model", "bundle"],
                    pos_op="and",
                )
                nodes_objects_temporary_by_type[typ] = tools.XML.extractor(
                    nodes_objects_by_type[typ],
                    pos_attrs=["model"],
                    neg_attrs=["bundle"],
                )
                nodes_objects_invalid_by_type[typ] = tools.XML.extractor(
                    nodes_objects_by_type[typ],
                    neg_attrs=["model", "bundle"],
                    neg_op="or",
                )
                data_objects_valid_by_type[typ] = tools.XML.enumerator(
                    nodes_objects_valid_by_type[typ], attr="name", mode=1
                )
                data_objects_temporary_by_type[typ] = tools.XML.enumerator(
                    nodes_objects_temporary_by_type[typ], attr="name", mode=1
                )
                data_objects_invalid_by_type[typ] = tools.XML.enumerator(
                    nodes_objects_invalid_by_type[typ],
                    attr="name",
                    mode=1,
                )
                data_objects_duplicate_by_type[typ] = []
                __available_objs = None
                __available_objs = (
                    data_objects_valid_by_type[typ]
                    + data_objects_temporary_by_type[typ]
                )
                __enum_data_objects = tools.XML.enumerator(
                    nodes_objects_by_type[typ], attr="name"
                )
                for obj in __available_objs:
                    if obj in __enum_data_objects:
                        __enum_data_objects.remove(obj)
                        continue
                    data_objects_duplicate_by_type[typ].append(obj)

                nodes_objects_duplicate_by_type[typ] = []
                nodes_objects_available_by_type[typ] = (
                    nodes_objects_valid_by_type[typ]
                    + nodes_objects_temporary_by_type[typ]
                )
                data_objects_available_by_type[typ] = tools.XML.enumerator(
                    nodes_objects_available_by_type[typ], attr="name", mode=1
                )
                for node in nodes_objects_available_by_type[typ]:
                    if node.get("name") in data_objects_duplicate_by_type[typ]:
                        nodes_objects_duplicate_by_type[typ].append(node)

            elif data_datasource == "OCMS2_0":
                data_objects_enum_model_by_type[typ] = tools.XML.enumerator(
                    nodes_objects_by_type[typ], attr="model"
                )
                nodes_objects_valid_by_type[typ] = tools.XML.extractor(
                    nodes_objects_by_type[typ],
                    pos_attrs=["model"],
                )
                nodes_objects_temporary_by_type[typ] = tools.XML.extractor(
                    nodes_objects_by_type[typ],
                    pos_attrs=["model"],
                    neg_attrs=["bundle"],
                )
                nodes_objects_invalid_by_type[typ] = tools.XML.extractor(
                    nodes_objects_by_type[typ],
                    neg_attrs=["model", "bundle"],
                    neg_op="or",
                )
                data_objects_valid_by_type[typ] = tools.XML.enumerator(
                    nodes_objects_valid_by_type[typ], attr="name", mode=1
                )
                data_objects_temporary_by_type[typ] = tools.XML.enumerator(
                    nodes_objects_temporary_by_type[typ], attr="name", mode=1
                )
                data_objects_invalid_by_type[typ] = tools.XML.enumerator(
                    nodes_objects_invalid_by_type[typ],
                    attr="name",
                    mode=1,
                )
                data_objects_duplicate_by_type[typ] = []
                __available_objs = None
                __available_objs = data_objects_temporary_by_type[typ]
                __enum_data_objects = tools.XML.enumerator(
                    nodes_objects_by_type[typ], attr="name"
                )
                for obj in __available_objs:
                    if obj in __enum_data_objects:
                        __enum_data_objects.remove(obj)
                        continue
                    data_objects_duplicate_by_type[typ].append(obj)

                nodes_objects_duplicate_by_type[typ] = []
                nodes_objects_available_by_type[typ] = nodes_objects_temporary_by_type[
                    typ
                ]
                data_objects_available_by_type[typ] = tools.XML.enumerator(
                    nodes_objects_available_by_type[typ], attr="name", mode=1
                )

                for node in nodes_objects_available_by_type[typ]:
                    if node.get("name") in data_objects_duplicate_by_type[typ]:
                        nodes_objects_duplicate_by_type[typ].append(node)

    tools.Logging.parse_xml_logger().info("Setting variables")
    prop.set_prop_nodes_objects_by_type(nodes_objects_by_type)
    prop.set_prop_nodes_objects_valid_by_type(nodes_objects_valid_by_type)
    prop.set_prop_nodes_objects_invalid_by_type(nodes_objects_invalid_by_type)
    prop.set_prop_nodes_objects_temporary_by_type(nodes_objects_temporary_by_type)
    prop.set_prop_nodes_objects_duplicate_by_type(nodes_objects_duplicate_by_type)
    prop.set_prop_nodes_objects_available_by_type(nodes_objects_available_by_type)
    prop.set_prop_data_objects_by_type(data_objects_by_type)
    prop.set_prop_data_objects_valid_by_type(data_objects_valid_by_type)
    prop.set_prop_data_objects_invalid_by_type(data_objects_invalid_by_type)
    prop.set_prop_data_objects_temporary_by_type(data_objects_temporary_by_type)
    prop.set_prop_data_objects_duplicate_by_type(data_objects_duplicate_by_type)
    prop.set_prop_data_objects_available_by_type(data_objects_available_by_type)
    prop.set_prop_data_objects_enum_model_by_type(data_objects_enum_model_by_type)
    prop.set_prop_data_objects_enum_bundle_by_type(data_objects_enum_bundle_by_type)

    tools.Logging.storage_logger().info("Updating storage xml data")
    from oe import storage

    storage.XMLData.purse()
    storage.XMLData.update(store.ParseXMLData)

    tools.Logging.gui_logger().info("Constructing dynamic ui group")
    construct_ui(self)


def construct_ui(self):
    p = self.parse
    tools.Logging.parse_xml_logger().info(
        "Notice: Current datasource is " + p.data_datasource
    )
    tools.Logging.gui_logger().info(
        "Notice: Some widgets may have some differences due to different datasource"
    )
    self.dynamic_box.add_group(
        id="點位物件統計", widget=qt.QtGroupVBoxCSWidget(text="點位物件統計")
    )
    self.dynamic_box.add_widget(
        parent_id="點位物件統計",
        id="物件數量",
        widget=qt.QtTextLineCSWidget(
            title="物件數量", text=len(p.nodes_objects).__str__(), readonly=True
        ),
    )
    self.dynamic_box.add_widget(
        parent_id="點位物件統計",
        id="分隔線1",
        widget=qt.QtLineCSWidget(),
    )
    self.dynamic_box.add_widget(
        parent_id="點位物件統計",
        id="Product Type",
        widget=qt.QtTextLineCSWidget(
            title="Product Type", text=p.data_datasource, readonly=True
        ),
    )
    self.dynamic_box.add_widget(
        parent_id="點位物件統計",
        id="分隔線2",
        widget=qt.QtLineCSWidget(),
    )
    self.dynamic_box.add_widget(
        parent_id="點位物件統計",
        id="// TAGS",
        widget=qt.QtTextLineCSWidget(
            title="// TAGS",
            text=tools.String.list_to_string(p.tags),
            readonly=True,
        ),
    )
    self.dynamic_box.add_widget(
        parent_id="點位物件統計",
        id="// ATTRS",
        widget=qt.QtTextLineCSWidget(
            title="// ATTRS",
            text=tools.String.list_to_string(p.attrs),
            readonly=True,
        ),
    )
    self.dynamic_box.add_widget(
        parent_id="點位物件統計",
        id="// TYPES",
        widget=qt.QtTextLineCSWidget(
            title="// TYPES",
            text=tools.String.list_to_string(p.types),
            readonly=True,
        ),
    )
    self.dynamic_box.add_widget(
        parent_id="點位物件統計",
        id="分隔線3",
        widget=qt.QtLineCSWidget(),
    )

    for typ in p.types:
        if typ not in p.non_device_types:
            self.dynamic_box.add_group(
                id=f"{typ} 物件", widget=qt.QtGroupVBoxCSWidget(text=f"{typ} 物件")
            )
            if p.data_datasource == "OCMS":
                self.dynamic_box.add_widget(
                    parent_id=f"{typ} 物件",
                    id=f"{typ} 數量",
                    widget=qt.QtTextLineCSWidget(
                        title=f"{typ} 數量",
                        text=[
                            tools.String.list_to_string(
                                p.props["data_objects_by_type"][typ]
                            ),
                            len(p.props["nodes_objects_by_type"][typ]).__str__(),
                        ],
                        readonly=True,
                        ratio=0.9,
                    ),
                )
                self.dynamic_box.add_widget(
                    parent_id=f"點位物件統計",
                    id=f"{typ} Bundle",
                    widget=qt.QtTextLineCSWidget(
                        title=f"{typ} Bundle",
                        text=[
                            tools.String.list_to_string(
                                p.props["data_objects_enum_bundle_by_type"][typ]
                            ),
                            len(
                                p.props["data_objects_enum_bundle_by_type"][typ]
                            ).__str__(),
                        ],
                        readonly=True,
                        ratio=0.9,
                    ),
                )
                self.dynamic_box.add_widget(
                    parent_id=f"點位物件統計",
                    id=f"{typ} Model",
                    widget=qt.QtTextLineCSWidget(
                        title=f"{typ} Model",
                        text=[
                            tools.String.list_to_string(
                                p.props["data_objects_enum_model_by_type"][typ]
                            ),
                            len(
                                p.props["data_objects_enum_model_by_type"][typ]
                            ).__str__(),
                        ],
                        readonly=True,
                        ratio=0.9,
                    ),
                )
                self.dynamic_box.add_widget(
                    parent_id=f"{typ} 物件",
                    id=f"{typ} 分隔線2",
                    widget=qt.QtLineCSWidget(),
                )
                self.dynamic_box.add_widget(
                    parent_id=f"{typ} 物件",
                    id=f"{typ} 核實設備",
                    widget=qt.QtTextLineCSWidget(
                        title=f"核實設備",
                        text=[
                            tools.String.list_to_string(
                                p.props["data_objects_valid_by_type"][typ]
                            ),
                            len(p.props["data_objects_valid_by_type"][typ]).__str__(),
                        ],
                        readonly=True,
                        ratio=0.9,
                    ),
                )
                _w = qt.QtTextLineCSWidget(
                    title=f"無效設備",
                    text=[
                        tools.String.list_to_string(
                            p.props["data_objects_invalid_by_type"][typ]
                        ),
                        len(p.props["data_objects_invalid_by_type"][typ]).__str__(),
                    ],
                    readonly=True,
                    ratio=0.9,
                )
                if len(p.props["data_objects_invalid_by_type"][typ]) > 0:
                    _w.set_status(qt.QtLineEditStatus.Error)
                self.dynamic_box.add_widget(
                    parent_id=f"{typ} 物件",
                    id=f"{typ} 無效設備",
                    widget=_w,
                )
                _w = qt.QtTextLineCSWidget(
                    title=f"暫代設備",
                    text=[
                        tools.String.list_to_string(
                            p.props["data_objects_temporary_by_type"][typ]
                        ),
                        len(p.props["data_objects_temporary_by_type"][typ]).__str__(),
                    ],
                    readonly=True,
                    ratio=0.9,
                )
                if len(p.props["data_objects_temporary_by_type"][typ]) > 0:
                    _w.set_status(qt.QtLineEditStatus.Error)
                self.dynamic_box.add_widget(
                    parent_id=f"{typ} 物件",
                    id=f"{typ} 暫代設備",
                    widget=_w,
                )
                self.dynamic_box.add_widget(
                    parent_id=f"{typ} 物件",
                    id=f"{typ} 分隔線3",
                    widget=qt.QtLineCSWidget(),
                )
                _w = qt.QtTextLineCSWidget(
                    title=f"重複設備",
                    text=[
                        tools.String.list_to_string(
                            p.props["data_objects_duplicate_by_type"][typ]
                        ),
                        len(p.props["data_objects_duplicate_by_type"][typ]).__str__(),
                    ],
                    readonly=True,
                    ratio=0.9,
                )
                if len(p.props["data_objects_duplicate_by_type"][typ]) > 0:
                    _w.set_status(qt.QtLineEditStatus.Warning)
                self.dynamic_box.add_widget(
                    parent_id=f"{typ} 物件",
                    id=f"{typ} 重複設備",
                    widget=_w,
                )

                if len(p.props["data_objects_invalid_by_type"][typ]) > 0:
                    self.dynamic_box.add_widget(
                        parent_id=f"{typ} 物件",
                        id=f"{typ} 無效設備提示",
                        widget=qt.QtInfoBoxCSWidget(
                            text="發現無效設備，請嘗試修正點位檔案（.xml）再重試一次，如有需要請連繫相關人員。",
                            status=qt.QtInfoBoxStatus.Error,
                        ),
                    )
                if len(p.props["data_objects_duplicate_by_type"][typ]) > 0:
                    self.dynamic_box.add_widget(
                        parent_id=f"{typ} 物件",
                        id=f"{typ} 重複設備提示",
                        widget=qt.QtInfoBoxCSWidget(
                            text="發現重複設備，請檢查重複的設備是否有必要修正。",
                            status=qt.QtInfoBoxStatus.Warning,
                        ),
                    )
                self.dynamic_box.add_widget(
                    parent_id=f"{typ} 物件",
                    id=f"{typ} OCMS提示",
                    widget=qt.QtInfoBoxCSWidget(
                        text="自 OCMS2.0 開始，由於部分屬性合併，＂各類 bundle＂、＂暫代設備＂將會被拿掉。",
                        status=qt.QtInfoBoxStatus.Help,
                    ),
                )
            elif p.data_datasource == "OCMS2_0":
                self.dynamic_box.add_widget(
                    parent_id=f"點位物件統計",
                    id=f"{typ} Model",
                    widget=qt.QtTextLineCSWidget(
                        title=f"{typ} Model",
                        text=[
                            tools.String.list_to_string(
                                p.props["data_objects_enum_model_by_type"][typ]
                            ),
                            len(
                                p.props["data_objects_enum_model_by_type"][typ]
                            ).__str__(),
                        ],
                        readonly=True,
                        ratio=0.9,
                    ),
                )
                self.dynamic_box.add_widget(
                    parent_id=f"{typ} 物件",
                    id=f"{typ} 數量",
                    widget=qt.QtTextLineCSWidget(
                        title=f"{typ} 數量",
                        text=[
                            tools.String.list_to_string(
                                p.props["data_objects_by_type"][typ]
                            ),
                            len(p.props["nodes_objects_by_type"][typ]).__str__(),
                        ],
                        readonly=True,
                        ratio=0.9,
                    ),
                )
                self.dynamic_box.add_widget(
                    parent_id=f"{typ} 物件",
                    id=f"{typ} 分隔線2",
                    widget=qt.QtLineCSWidget(),
                )
                self.dynamic_box.add_widget(
                    parent_id=f"{typ} 物件",
                    id=f"{typ} 核實設備",
                    widget=qt.QtTextLineCSWidget(
                        title=f"核實設備",
                        text=[
                            tools.String.list_to_string(
                                p.props["data_objects_valid_by_type"][typ]
                            ),
                            len(p.props["data_objects_valid_by_type"][typ]).__str__(),
                        ],
                        readonly=True,
                        ratio=0.9,
                    ),
                )
                _w = qt.QtTextLineCSWidget(
                    title=f"無效設備",
                    text=[
                        tools.String.list_to_string(
                            p.props["data_objects_invalid_by_type"][typ]
                        ),
                        len(p.props["data_objects_invalid_by_type"][typ]).__str__(),
                    ],
                    readonly=True,
                    ratio=0.9,
                )
                if len(p.props["data_objects_invalid_by_type"][typ]) > 0:
                    _w.set_status(qt.QtLineEditStatus.Error)
                self.dynamic_box.add_widget(
                    parent_id=f"{typ} 物件",
                    id=f"{typ} 無效設備",
                    widget=_w,
                )
                self.dynamic_box.add_widget(
                    parent_id=f"{typ} 物件",
                    id=f"{typ} 分隔線3",
                    widget=qt.QtLineCSWidget(),
                )
                _w = qt.QtTextLineCSWidget(
                    title=f"重複設備",
                    text=[
                        tools.String.list_to_string(
                            p.props["data_objects_duplicate_by_type"][typ]
                        ),
                        len(p.props["data_objects_duplicate_by_type"][typ]).__str__(),
                    ],
                    readonly=True,
                    ratio=0.9,
                )
                if len(p.props["data_objects_duplicate_by_type"][typ]) > 0:
                    _w.set_status(qt.QtLineEditStatus.Warning)
                self.dynamic_box.add_widget(
                    parent_id=f"{typ} 物件",
                    id=f"{typ} 重複設備",
                    widget=_w,
                )
                if len(p.props["data_objects_invalid_by_type"][typ]) > 0:
                    self.dynamic_box.add_widget(
                        parent_id=f"{typ} 物件",
                        id=f"{typ} 無效設備提示",
                        widget=qt.QtInfoBoxCSWidget(
                            text="發現無效設備，請嘗試修正點位檔案（.xml）再重試一次，如有需要請連繫相關人員。",
                            status=qt.QtInfoBoxStatus.Error,
                        ),
                    )
                if len(p.props["data_objects_duplicate_by_type"][typ]) > 0:
                    self.dynamic_box.add_widget(
                        parent_id=f"{typ} 物件",
                        id=f"{typ} 重複設備提示",
                        widget=qt.QtInfoBoxCSWidget(
                            text="發現重複設備，請檢查重複的設備是否有必要修正。",
                            status=qt.QtInfoBoxStatus.Warning,
                        ),
                    )
    tools.Logging.gui_logger().info("Completed constructing dynamic ui group manager")
