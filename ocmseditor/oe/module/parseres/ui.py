import ocmseditor.oe.qt as qt
import ocmseditor.tool as tool
import ocmseditor.oe.helper as helper
import ocmseditor.oe.data.const as const

from . import operator


class ParseResourceCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parsed = False

        self.set_text("Resource 分析")

        self.scrollarea = qt.QtScrollareaCSWidget()
        self.scrollarea.setSizePolicy(
            qt.QtWidgets.QSizePolicy.Expanding,
            qt.QtWidgets.QSizePolicy.MinimumExpanding,
        )

        self.groupbox_manager = qt.QtGroupboxManager()

        self.resource_dir_box = qt.QtGroupHBoxCSWidget()
        self.resource_dir_box.set_text("Resource 路徑")

        self.resource_log_box = qt.QtGroupHBoxCSWidget()
        self.resource_log_box.set_text("Resource 處理紀錄")

        self.resource_import_box = qt.QtGroupHBoxCSWidget()
        self.resource_import_box.layout.setContentsMargins(0, 0, 0, 0)

        self.fetch_btn = qt.QtButtonCSWidget()
        self.fetch_btn.set_width(4)
        self.fetch_btn.set_height(16)
        self.fetch_btn.set_tooltip("Fetch️")

        self.resource_dir_txt = qt.QtTextLineCSWidget()
        self.resource_dir_txt.set_text("")
        self.resource_dir_txt.lineedit.setReadOnly(True)

        self.parse_btn = qt.QtButtonCSWidget()
        self.parse_btn.set_icon(":/out_multDoubleLinear.png")
        self.parse_btn.set_text("  分析")
        self.parse_btn.set_width(80)
        self.parse_btn.set_height(32)

        self.browse_btn = qt.QtButtonCSWidget()
        self.browse_btn.set_icon("open_folder.png")
        self.browse_btn.set_text("")
        self.browse_btn.set_height(32)

        self.write_log_btn = qt.QtButtonCSWidget()
        self.write_log_btn.set_icon(":/fileSave.png")
        self.write_log_btn.set_text("  匯出所有")
        self.write_log_btn.set_height(20)

        self.write_single_log_btn = qt.QtButtonCSWidget()
        self.write_single_log_btn.set_icon(":/fileSave.png")
        self.write_single_log_btn.set_text("  匯出單個")
        self.write_single_log_btn.set_height(20)
        self.write_single_log_btn.set_width(110)

        self.fetch_btn.clicked.connect(lambda: operator.op_fetch_resource_path(self))
        self.parse_btn.clicked.connect(lambda: operator.op_parse(self))
        self.browse_btn.clicked.connect(lambda: operator.op_browser_resource_path(self))
        self.write_log_btn.clicked.connect(lambda: operator.op_write_datasheet(self))
        self.write_single_log_btn.clicked.connect(
            lambda: operator.op_write_datasheet(self, 1)
        )

        self.resource_dir_box.layout.addWidget(self.fetch_btn)
        self.resource_dir_box.layout.addWidget(self.resource_dir_txt)
        self.resource_dir_box.layout.addWidget(self.parse_btn)
        self.resource_dir_box.layout.addWidget(self.browse_btn)
        self.resource_dir_box.layout.addWidget(self.browse_btn)
        self.resource_log_box.layout.addWidget(self.write_log_btn)
        self.resource_log_box.layout.addWidget(self.write_single_log_btn)

        self.scrollarea.layout.addWidget(self.resource_dir_box)
        self.scrollarea.layout.addWidget(self.resource_log_box)
        self.scrollarea.layout.addWidget(self.groupbox_manager.get_groupbox())

        self.frame_layout.addWidget(self.scrollarea)

        self._validate()

    def _destroy(self):
        self.groupbox_manager.clear_all()

    def _validate(self):
        helper.Logger.info(__name__, "Validating resource directory")

        resource_path = tool.Registry.get_reg(const.REG_RES_PATH)
        ocms = tool.OCMS.get_ocms()
        if (
            not tool.File.exists(resource_path)
            or not tool.File.is_dir(resource_path)
            or not ocms.xml.valid()
        ):
            tool.Widget.disable(self.parse_btn)
        else:
            tool.Widget.enable(self.parse_btn)

        if not self.parsed:
            tool.Widget.disable(self.write_log_btn)
            tool.Widget.disable(self.write_single_log_btn)
        else:
            tool.Widget.enable(self.write_log_btn)
            tool.Widget.enable(self.write_single_log_btn)

        self._preconstruct(resource_path)

    def _preconstruct(self, resource_dir):
        tool.Widget.set_text(self.resource_dir_txt.lineedit, resource_dir)

    def _construct(self):
        helper.Logger.info(__name__, "Constructing")
        ocms = tool.OCMS.get_ocms()
        store = ocms.res

        sort = store.collect_data.get("sort")
        stats = store.collect_data.get("stats")

        self.groupbox_manager.add_group(
            widget_id="模型檔統計", widget=qt.QtGroupVBoxCSWidget(text="模型檔統計")
        )

        self.groupbox_manager.add_widget(
            parent_id="模型檔統計",
            widget_id="所有檔案",
            widget=qt.QtTextLineCSWidget(
                title="所有檔案",
                text=stats.get("total_scan_files").__str__(),
                readonly=True,
            ),
        )
        self.groupbox_manager.add_widget(
            parent_id="模型檔統計",
            widget_id="所有模型",
            widget=qt.QtTextLineCSWidget(
                title="所有模型",
                text=stats.get("total_models").__str__(),
                readonly=True,
            ),
        )
        self.groupbox_manager.add_widget(
            parent_id="模型檔統計",
            widget_id="已核實的模型",
            widget=qt.QtTextLineCSWidget(
                title="已核實的模型",
                text=stats.get("total_valid_models").__str__(),
                readonly=True,
                status=qt.QtLineEditStatus.Success,
            ),
        )
        self.groupbox_manager.add_widget(
            parent_id="模型檔統計",
            widget_id="分隔線1",
            widget=qt.QtLineCSWidget(),
        )
        self.groupbox_manager.add_widget(
            parent_id="模型檔統計",
            widget_id="核實模型排序",
            widget=qt.QtTextLineCSWidget(
                title="核實模型排序",
                text=tool.String.dict_to_string(sort.get("size")),
                readonly=True,
            ),
        )

        self.groupbox_manager.add_group(
            widget_id="模型路徑面板", widget=qt.QtGroupVBoxCSWidget(text="模型路徑面板")
        )

        _tree = qt.QtTreeCSWidget()
        _tree.setToolTip("🖱️ 雙擊滑鼠左鍵開啟模型所在目錄（LMB + LMB）")
        _tree.setHeaderLabels(["模型", "檔案路徑"])
        header = _tree.header()
        header.setSectionResizeMode(1, qt.QtWidgets.QHeaderView.Stretch)
        _tree.setIndentation(2)
        self.groupbox_manager.add_widget(
            parent_id="模型路徑面板",
            widget_id="樹狀清單",
            widget=_tree,
        )

        errors = stats.get("total_models") - stats.get("total_valid_models")

        for index, (model, data) in enumerate(store.parse_data.items()):
            _item = [model, data.get("path")]
            _treeitem = qt.QtTreeItemCSWidget(_item)
            _treeitem.tree = _tree
            _tree.addTopLevelItem(_treeitem)

            _browser_btn = qt.QtButtonCSWidget()
            _browser_btn.set_text("瀏覽")

            if data.get("file").get("path") != "":
                _treeitem.setText(1, data.get("file").get("path"))
                _treeitem.matched = True
            else:
                _treeitem.setText(1, "找不到路徑")
                _treeitem.set_status(_treeitem.status.Missing)

        _infobox = qt.QtInfoBoxCSWidget(
            text=f"剩餘 {errors} 個模型找不到路徑，請解決問題後重新分析。",
            height=32,
            status=qt.QtInfoBoxStatus.Warning,
        )
        _infobox2 = qt.QtInfoBoxCSWidget(
            text=f"仍有問題導致無法匯入模型！",
            height=32,
            status=qt.QtInfoBoxStatus.Error,
        )

        if errors > 0:
            _infobox.label.setText(f"剩餘 {errors} 個模型找不到路徑，請解決問題後重新分析。")
            _infobox.set_status(qt.QtInfoBoxStatus.Warning)
            _infobox2.label.setText("仍有問題導致無法匯入模型！")
            _infobox2.set_status(qt.QtInfoBoxStatus.Error)
        else:
            _infobox.label.setText("所有模型都已找到路徑。")
            _infobox.set_status(qt.QtInfoBoxStatus.Success)
            _infobox2.label.setText("已準備就緒，可以開始匯入模型。")
            _infobox2.set_status(qt.QtInfoBoxStatus.Success)

        self.groupbox_manager.add_widget(
            parent_id="模型路徑面板",
            widget_id="剩餘的錯誤數量提示",
            widget=_infobox,
        )
        self.groupbox_manager.add_widget(
            parent_id="模型路徑面板",
            widget_id="匯入模型確認提示",
            widget=_infobox2,
        )

        helper.Logger.info(__name__, "Completed constructing dynamic ui group manager")

        helper.Logger.info(__name__, "Finished constructing types of widgets")
        import ocmseditor.oe.ui as global_ui

        helper.Logger.info(__name__, "Starting to update top level ui")
        global_ui.update_top_level_ui()
        # helper.Log.info(__name__, "Starting to toggle frame expand by widget")
        # global_ui.toggle_frame_expand_by_widget(self)
        helper.Logger.info(__name__, "Finished constructing widgets")
