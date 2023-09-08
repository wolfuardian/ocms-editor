import os

import oe.tools as tools
import oe.storage as storage
import oe.core.maya as core

from oe.utils import qt
from oe.utils import const as c
from . import store, prop


def op_fetch_res_dir(self):
    tools.Log.info(__name__, "Fetching resources directory")

    validate_resources_dir(self)


def op_init_res_dir(self):
    tools.Log.info(__name__, "Initializing resources source directory")

    op_browser_resources_dir(self)


def op_browser_resources_dir(self):
    tools.Log.info(__name__, "Browsing resources directory")

    sel_path = core.browser(storage, tools, c.REG_RES_DIR, 3)

    validate_resources_dir(self)

    storage.Widget(self.resource_dir_txt.lineedit).set_text(sel_path)

    storage.Widget(self.resource_dir_txt).show()
    storage.Widget(self.init_btn).hide()
    storage.Widget(self.browse_btn).show()
    storage.Widget(self.parse_btn).show()


def op_parse_resources(self):
    tools.Log.info(__name__, "Parsing resources")

    parse_resources(self)


def validate_resources_dir(self):
    tools.Log.info(__name__, "Validating resources directory")

    _resources_dir = storage.Registry(c.REG_RES_DIR).get()
    _xml_path = storage.Registry(c.REG_XML_PATH).get()
    if (
        not storage.Path(_resources_dir).is_valid()
        or not storage.Path(_resources_dir).is_dir()
        or not storage.XMLData.is_valid()
    ):
        storage.Widget(self.parse_btn).disable()
        storage.ResourcesData.close()
    else:
        storage.Widget(self.parse_btn).enable()
        storage.ResourcesData.open()

    _setup_ui(self, _resources_dir)


def _setup_ui(self, _resources_dir):
    tools.Log.info(__name__, "Setting up resources directory ui")

    storage.Widget(self.resource_dir_txt.lineedit).set_text(_resources_dir)
    storage.Widget(self.resource_dir_txt).show()
    storage.Widget(self.init_btn).hide()
    storage.Widget(self.browse_btn).show()
    storage.Widget(self.parse_btn).show()


def parse_resources(self):
    tools.Log.info(__name__, "Initializing dynamic ui group manager")
    self.groupvbox.clear_all()

    tools.Log.info(__name__, "Initializing parse resources data")
    self.parse = store.ParseResourcesData()

    _dir = tools.Registry.get_value(c.REG_KEY, c.REG_SUB, c.REG_RES_DIR, "")

    tools.Log.info(__name__, "Loading resources directory")
    self.parse.load(_dir)

    tools.Log.info(__name__, "Starting constructing variables")
    models_paths = self.parse.models_paths
    models_paths_sorted_by_size = self.parse.models_paths_sorted_by_size
    models_paths_sorted_filenames = self.parse.models_paths_sorted_filenames
    models_paths_sorted_filesizes = self.parse.models_paths_sorted_filesizes
    models_names_mapping_by_type = {}
    models_paths_mapping_by_type = {}

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

    tools.Log.info(__name__, "Setting variables")
    prop.set_prop_models_names_mapping_by_type(models_names_mapping_by_type)
    prop.set_prop_models_paths_mapping_by_type(models_paths_mapping_by_type)

    # Storage
    tools.Log.info(__name__, "Saving resources data")
    storage.ResourcesData.purse()
    storage.ResourcesData.update(store.ParseResourcesData)

    tools.Log.info(__name__, "Constructing dynamic ui group")
    construct_ui(self)


def construct_ui(self):
    p: store.ParseResourcesData = self.parse
    tools.Log.info(__name__, "Constructing dynamic ui group manager")
    self.groupvbox.add_group(id="模型檔統計", widget=qt.QtGroupVBoxCSWidget(text="模型檔統計"))

    self.groupvbox.add_widget(
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
    self.groupvbox.add_widget(
        parent_id="模型檔統計",
        id="所有模型數量",
        widget=qt.QtTextLineCSWidget(
            title="所有模型數量",
            text=len(p.models_paths).__str__(),
            readonly=True,
        ),
    )
    self.groupvbox.add_widget(
        parent_id="模型檔統計",
        id="分隔線1",
        widget=qt.QtLineCSWidget(),
    )

    self.groupvbox.add_widget(
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

    self.groupvbox.add_group(id="模型分析", widget=qt.QtGroupVBoxCSWidget(text="模型分析"))

    _tree = qt.QtTreeCSWidget()
    _tree.setHeaderLabels(["模型目錄", "檔案路徑"])
    header = _tree.header()
    header.setSectionResizeMode(1, qt.QtWidgets.QHeaderView.Stretch)
    _tree.setIndentation(2)
    self.groupvbox.add_widget(
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
        self.groupvbox.add_widget(
            parent_id="模型檔統計",
            id=f"各類 {typ}",
            widget=qt.QtTextLineCSWidget(
                title=f"各類 {typ}",
                text=[tools.String.list_to_string(models), len(models).__str__()],
                readonly=True,
                ratio=0.9,
            ),
        )

        # p.props["models_names_mapping_by_type"][typ] = {
        #     (model.split("/")[-1] if "/" in model else model).lower(): model
        #     for model in models
        # }
        # p.props["models_paths_mapping_by_type"][typ] = {
        #     os.path.splitext(os.path.basename(path))[0].lower(): path
        #     for path in p.models_paths
        # }

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

    self.groupvbox.add_widget(
        parent_id="模型分析",
        id="剩餘的錯誤數量提示",
        widget=_infobox,
    )

    _btn = qt.QtButtonCSWidget(text="重新查找目錄並更新列表")
    _btn.clicked.connect(lambda: parse_resources(self))

    self.groupvbox.add_widget(
        parent_id="模型分析",
        id="更新列表 ( 將不保留變更 )",
        widget=_btn,
    )

    tools.Log.info(__name__, "Completed constructing dynamic ui group manager")
