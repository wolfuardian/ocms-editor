import copy
import os

import oe.tools as tools
import oe.storage as storage

from oe.utils import qt
from oe.refer import Registry as reg_
from . import store, prop


def op_initialize_resources_source_dir(self):
    tools.Logging.parse_resources_logger().info("Initializing resources source directory")

    _default_dir = tools.Registry.get_value(
        reg_.REG_KEY, reg_.REG_SUB, reg_.REG_RES_SRC_DIR, ""
    )
    if _default_dir == "":
        _target_dir = tools.Registry.set_value(
            reg_.REG_KEY,
            reg_.REG_SUB,
            reg_.REG_RES_SRC_DIR,
            tools.Maya.browser(3, _default_dir),
        )
        self.txt_res_src_dir.lineedit.setText(_target_dir)
    else:
        self.txt_res_src_dir.lineedit.setText(_default_dir)
    self.btn_init_res_src_dir.set_force_visible(False)
    self.txt_res_src_dir.set_force_visible(True)
    self.txt_res_src_dir.lineedit.setCursorPosition(0)
    self.btn_browser_res_src_dir.set_force_visible(True)
    tools.Logging.parse_resources_logger().info(
        "Completed initializing resources source directory"
    )

    parse_resources(self)


def op_browser_resources_source_dir(self):
    tools.Logging.parse_resources_logger().info("Browsing resources source directory")

    _default_dir = tools.Registry.get_value(
        reg_.REG_KEY, reg_.REG_SUB, reg_.REG_RES_SRC_DIR, ""
    )
    _browser_dir = tools.Maya.browser(3, _default_dir)
    if _browser_dir == "":
        tools.Logging.parse_resources_logger().warning("User canceled the browser dialog.")
        return
    _target_dir = tools.Registry.set_value(
        reg_.REG_KEY,
        reg_.REG_SUB,
        reg_.REG_RES_SRC_DIR,
        _browser_dir,
    )
    self.txt_res_src_dir.lineedit.setText(_target_dir)
    self.txt_res_src_dir.lineedit.setCursorPosition(0)
    tools.Logging.parse_resources_logger().info(
        "Completed browsing resources source directory"
    )

    parse_resources(self)


def parse_resources(self):
    # <editor-fold desc="CODE_BLOCK: DEBUG_MODE">
    from oe.module.parsexml import operator as xml_op
    xml_op.op_initialize_xml_path(storage.UIData.ui["frame_parse_xml"])
    # </editor-fold>

    tools.Logging.gui_logger().info("Initializing dynamic ui group manager")
    self.dynamic_box.clear_all()

    tools.Logging.parse_resources_logger().info("Initializing parse resources data")
    self.parse = store.ParseResourcesData()

    _dir = tools.Registry.get_value(
        reg_.REG_KEY, reg_.REG_SUB, reg_.REG_RES_SRC_DIR, ""
    )

    tools.Logging.parse_resources_logger().info("Loading resources directory")
    self.parse.load(_dir)

    tools.Logging.parse_resources_logger().info("Starting constructing variables")
    models_paths = self.parse.models_paths
    models_paths_sorted_by_size = self.parse.models_paths_sorted_by_size
    models_paths_sorted_filenames = self.parse.models_paths_sorted_filenames
    models_paths_sorted_filesizes = self.parse.models_paths_sorted_filesizes
    models_names_mapping_by_type = {}
    models_paths_mapping_by_type = {}
    models_paths_changed_by_type = {}

    _tmp_enum_models_by_type = {}
    if storage.XMLData.data_datasource == "OCMS":
        _tmp_enum_models_by_type = storage.XMLData.props[
            "data_objects_enum_bundle_by_type"
        ]
    elif storage.XMLData.data_datasource == "OCMS2_0":
        _tmp_enum_models_by_type = storage.XMLData.props[
            "data_objects_enum_model_by_type"
        ]

    for index, (typ, models) in enumerate(_tmp_enum_models_by_type.items()):
        models_names_mapping_by_type[typ] = {
            (model.split("/")[-1] if "/" in model else model).lower(): model
            for model in models
        }
        models_paths_mapping_by_type[typ] = {
            os.path.splitext(os.path.basename(path))[0].lower(): path
            for path in models_paths
        }

        _tmp_models_names = dict(models_names_mapping_by_type[typ])
        _tmp_models_paths = dict(models_paths_mapping_by_type[typ])

        models_paths_mapping_by_type[typ].clear()

        for name, model in _tmp_models_names.items():
            if name in _tmp_models_paths.keys():
                models_paths_mapping_by_type[typ][name] = _tmp_models_paths[name]
            else:
                models_paths_mapping_by_type[typ][name] = ""

    models_paths_changed_by_type = copy.deepcopy(models_paths_mapping_by_type)

    tools.Logging.parse_resources_logger().info("Setting variables")
    prop.set_prop_models_names_mapping_by_type(models_names_mapping_by_type)
    prop.set_prop_models_paths_mapping_by_type(models_paths_mapping_by_type)
    prop.set_prop_models_paths_changed_by_type(models_paths_changed_by_type)

    construct_ui(self)


def construct_ui(self):
    p: store.ParseResourcesData = self.parse
    tools.Logging.gui_logger().info("Constructing dynamic ui group manager")
    self.dynamic_box.add_group(id="模型檔統計", widget=qt.QtGroupVBoxCSWidget(text="模型檔統計"))

    self.dynamic_box.add_widget(
        parent_id="模型檔統計",
        id="所有模型 (由大到小)",
        widget=qt.QtTextLineCSWidget(
            title="所有模型 (由大到小)",
            text=tools.String.dict_to_string(
                tools.Dictionary.create_dict_from_lists(
                    p.models_paths_sorted_filenames, p.models_paths_sorted_filesizes
                )
            ),
            readonly=True,
        ),
    )
    self.dynamic_box.add_widget(
        parent_id="模型檔統計",
        id="所有模型數量",
        widget=qt.QtTextLineCSWidget(
            title="所有模型數量",
            text=len(p.models_paths).__str__(),
            readonly=True,
        ),
    )
    self.dynamic_box.add_widget(
        parent_id="模型檔統計",
        id="分隔線1",
        widget=qt.QtLineCSWidget(),
    )

    self.dynamic_box.add_widget(
        parent_id="模型檔統計",
        id="各類模型數量",
        widget=qt.QtTextLineCSWidget(
            title="各類模型數量",
            text=sum(
                [
                    len(val)
                    for val in storage.XMLData.props[
                        "data_objects_enum_model_by_type"
                    ].values()
                ]
            ).__str__(),
            readonly=True,
        ),
    )

    self.dynamic_box.add_group(id="模型分析", widget=qt.QtGroupVBoxCSWidget(text="模型分析"))

    _tree = qt.QtTreeCSWidget()
    _tree.setHeaderLabels(["模型目錄", "檔案路徑"])
    header = _tree.header()
    header.setSectionResizeMode(1, qt.QtWidgets.QHeaderView.Stretch)
    _tree.setIndentation(2)
    self.dynamic_box.add_widget(
        parent_id="模型分析",
        id="樹狀清單",
        widget=_tree,
    )
    _tmp_enum_models_by_type = {}
    if storage.XMLData.data_datasource == "OCMS":
        _tmp_enum_models_by_type = storage.XMLData.props[
            "data_objects_enum_bundle_by_type"
        ]
    elif storage.XMLData.data_datasource == "OCMS2_0":
        _tmp_enum_models_by_type = storage.XMLData.props[
            "data_objects_enum_model_by_type"
        ]

    _error_count = 0
    for index, (typ, models) in enumerate(_tmp_enum_models_by_type.items()):
        self.dynamic_box.add_widget(
            parent_id="模型檔統計",
            id=f"各類 {typ}",
            widget=qt.QtTextLineCSWidget(
                title=f"各類 {typ}",
                text=[tools.String.list_to_string(models), len(models).__str__()],
                readonly=True,
                ratio=0.9,
            ),
        )

        p.props["models_names_mapping_by_type"][typ] = {
            (model.split("/")[-1] if "/" in model else model).lower(): model
            for model in models
        }
        p.props["models_paths_mapping_by_type"][typ] = {
            os.path.splitext(os.path.basename(path))[0].lower(): path
            for path in p.models_paths
        }

        _tmp_models_names = dict(p.props["models_names_mapping_by_type"][typ])
        _tmp_models_paths = dict(p.props["models_paths_mapping_by_type"][typ])

        for name, model in _tmp_models_names.items():
            _treeitem = qt.QtTreeItemCSWidget([model, "__path__"])
            _treeitem.tree = _tree
            _tree.addTopLevelItem(_treeitem)

            if name in _tmp_models_paths.keys():
                _treeitem.setText(1, p.props["models_paths_mapping_by_type"][typ][name])
                _treeitem.is_match = True
                _treeitem.matched_path = p.props["models_paths_mapping_by_type"][typ][
                    name
                ]
            else:
                _error_count += 1
                _treeitem.setText(1, "找不到路徑")
                _treeitem.set_status(_treeitem.status.Missing)

    _infobox = qt.QtInfoBoxCSWidget(
        text=f"剩餘 {_error_count} 個模型找不到路徑，請重新查找目錄並更新列表。",
        status=qt.QtInfoBoxStatus.Warning,
    )

    if _error_count == 0:
        _infobox.label.setText("所有模型都已找到路徑。")
        _infobox.set_status(qt.QtInfoBoxStatus.Success)

    self.dynamic_box.add_widget(
        parent_id="模型分析",
        id="剩餘的錯誤數量提示",
        widget=_infobox,
    )

    _btn = qt.QtButtonCSWidget(text="重新查找目錄並更新列表")
    _btn.clicked.connect(lambda: parse_resources(self))

    self.dynamic_box.add_widget(
        parent_id="模型分析",
        id="更新列表 ( 將不保留變更 )",
        widget=_btn,
    )

    tools.Logging.gui_logger().info("Completed constructing dynamic ui group manager")
