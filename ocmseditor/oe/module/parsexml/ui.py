import ocmseditor.oe.qt as qt
import ocmseditor.tool as tool
import ocmseditor.oe.helper as helper
import ocmseditor.oe.data.const as const

from . import operator


class ParseXMLCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parsed = False

        self.set_text("XML 分析")

        self.scrollarea = qt.QtScrollareaCSWidget()
        self.scrollarea.setSizePolicy(
            qt.QtWidgets.QSizePolicy.Expanding, qt.QtWidgets.QSizePolicy.Expanding
        )

        self.groupbox_manager = qt.QtGroupboxManager()

        self.xml_path_box = qt.QtGroupHBoxCSWidget()
        self.xml_path_box.set_text("XML 路徑")

        self.xml_log_box = qt.QtGroupHBoxCSWidget()
        self.xml_log_box.set_text("XML 處理紀錄")

        self.fetch_btn = qt.QtButtonCSWidget()
        self.fetch_btn.set_width(4)
        self.fetch_btn.set_height(16)
        self.fetch_btn.set_tooltip("Fetch")

        self.xml_path_txt = qt.QtTextLineCSWidget()
        self.xml_path_txt.set_text("")
        self.xml_path_txt.lineedit.setReadOnly(True)

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

        self.fetch_btn.clicked.connect(lambda: operator.op_fetch_xml_filepath(self))
        self.parse_btn.clicked.connect(lambda: operator.op_parse_xml(self))
        self.browse_btn.clicked.connect(lambda: operator.op_browser_xml_filepath(self))
        self.write_log_btn.clicked.connect(
            lambda: operator.op_write_ocms_datasheet(self)
        )
        self.write_single_log_btn.clicked.connect(
            lambda: operator.op_write_ocms_datasheet(self, 1)
        )

        self.xml_path_box.layout.addWidget(self.fetch_btn)
        self.xml_path_box.layout.addWidget(self.xml_path_txt)
        self.xml_path_box.layout.addWidget(self.parse_btn)
        self.xml_path_box.layout.addWidget(self.browse_btn)
        self.xml_log_box.layout.addWidget(self.write_log_btn)
        self.xml_log_box.layout.addWidget(self.write_single_log_btn)
        self.scrollarea.layout.addWidget(self.xml_path_box)
        self.scrollarea.layout.addWidget(self.xml_log_box)
        self.scrollarea.layout.addWidget(self.groupbox_manager.get_groupbox())

        self.frame_layout.addWidget(self.scrollarea)

        self._validate()

    def _destroy(self):
        self.groupbox_manager.clear_all()

    def _validate(self):
        xml_path = tool.Registry.get_reg(const.REG_XML_FILEPATH)
        if (
            not tool.File.exists(xml_path)
            or not tool.File.is_file(xml_path)
            or not tool.File.is_xml(xml_path)
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
        self._preconstruct(xml_path)

    def _preconstruct(self, xml_path):
        tool.Widget.set_text(self.xml_path_txt.lineedit, xml_path)

    def _construct(self):
        helper.Logger.info(__name__, "Constructing widgets")
        helper.Logger.info(__name__, "Fetching OCMSStore instance")
        ocms = tool.OCMS.get_ocms()
        store = ocms.xml
        helper.Logger.info(
            __name__, "Notice: Current datasource is " + store.product_type
        )
        helper.Logger.info(
            __name__,
            "Notice: Some widgets may have some differences due to different datasource",
        )
        self.groupbox_manager.add_group(
            widget_id="點位物件統計", widget=qt.QtGroupVBoxCSWidget(text="點位物件統計")
        )

        self.groupbox_manager.add_widget(
            parent_id="點位物件統計",
            widget_id="所有物件總量",
            widget=qt.QtTextLineCSWidget(
                title="所有物件總量", text=len(store.parse_data).__str__(), readonly=True
            ),
        )
        self.groupbox_manager.add_widget(
            parent_id="點位物件統計",
            widget_id="分隔線0",
            widget=qt.QtLineCSWidget(),
        )
        self.groupbox_manager.add_widget(
            parent_id="點位物件統計",
            widget_id="非設備數量",
            widget=qt.QtTextLineCSWidget(
                title="非設備數量",
                text=len(store.collect_data.get("object").get("non_devices")).__str__(),
                readonly=True,
            ),
        )
        self.groupbox_manager.add_widget(
            parent_id="點位物件統計",
            widget_id="設備數量",
            widget=qt.QtTextLineCSWidget(
                title="設備數量",
                text=(
                    len(store.parse_data)
                    - len(store.collect_data.get("object").get("non_devices"))
                ).__str__(),
                readonly=True,
            ),
        )
        self.groupbox_manager.add_widget(
            parent_id="點位物件統計",
            widget_id="分隔線1",
            widget=qt.QtLineCSWidget(),
        )
        self.groupbox_manager.add_widget(
            parent_id="點位物件統計",
            widget_id="Product Type",
            widget=qt.QtTextLineCSWidget(
                title="Product Type", text=store.product_type, readonly=True
            ),
        )
        self.groupbox_manager.add_widget(
            parent_id="點位物件統計",
            widget_id="分隔線2",
            widget=qt.QtLineCSWidget(),
        )
        self.groupbox_manager.add_widget(
            parent_id="點位物件統計",
            widget_id="// TAGS",
            widget=qt.QtTextLineCSWidget(
                title="// TAGS",
                text=tool.String.list_to_string(
                    store.collect_data.get("object").get("tags")
                ),
                readonly=True,
            ),
        )
        self.groupbox_manager.add_widget(
            parent_id="點位物件統計",
            widget_id="// ATTRS",
            widget=qt.QtTextLineCSWidget(
                title="// ATTRS",
                text=tool.String.list_to_string(
                    store.collect_data.get("object").get("attributes")
                ),
                readonly=True,
            ),
        )
        self.groupbox_manager.add_widget(
            parent_id="點位物件統計",
            widget_id="// TYPES",
            widget=qt.QtTextLineCSWidget(
                title="// TYPES",
                text=tool.String.list_to_string(
                    store.collect_data.get("object").get("types")
                ),
                readonly=True,
            ),
        )
        self.groupbox_manager.add_widget(
            parent_id="點位物件統計",
            widget_id="分隔線3",
            widget=qt.QtLineCSWidget(),
        )

        types = store.collect_data.get("object").get("types")

        helper.Logger.info(__name__, "Constructing types of widgets")
        for typ in types:
            if typ not in store.config.get("non_device_type"):
                self.groupbox_manager.add_group(
                    widget_id=f"{typ} 物件",
                    widget=qt.QtGroupVBoxCSWidget(text=f"{typ} 物件"),
                )
                if store.product_type == "OCMS":
                    self.groupbox_manager.add_widget(
                        parent_id=f"{typ} 物件",
                        widget_id=f"{typ} 數量",
                        widget=qt.QtTextLineCSWidget(
                            title=f"{typ} 數量",
                            text=[
                                tool.String.list_to_string(
                                    tool.XML.query_elems_attrs(
                                        store.collect_data.get("type_of")
                                        .get("element")
                                        .get(typ),
                                        attr="name",
                                    )
                                ),
                                len(
                                    store.collect_data.get("type_of")
                                    .get("element")
                                    .get(typ)
                                ).__str__(),
                            ],
                            readonly=True,
                            ratio=0.9,
                        ),
                    )
                    self.groupbox_manager.add_widget(
                        parent_id=f"點位物件統計",
                        widget_id=f"{typ} Bundle",
                        widget=qt.QtTextLineCSWidget(
                            title=f"{typ} Bundle",
                            text=[
                                tool.String.list_to_string(
                                    store.collect_data.get("type_of")
                                    .get("bundle")
                                    .get(typ)
                                ),
                                len(
                                    store.collect_data.get("type_of")
                                    .get("bundle")
                                    .get(typ)
                                ).__str__(),
                            ],
                            readonly=True,
                            ratio=0.9,
                        ),
                    )
                    self.groupbox_manager.add_widget(
                        parent_id=f"點位物件統計",
                        widget_id=f"{typ} Model",
                        widget=qt.QtTextLineCSWidget(
                            title=f"{typ} Model",
                            text=[
                                tool.String.list_to_string(
                                    store.collect_data.get("type_of")
                                    .get("model")
                                    .get(typ)
                                ),
                                len(
                                    store.collect_data.get("type_of")
                                    .get("model")
                                    .get(typ)
                                ).__str__(),
                            ],
                            readonly=True,
                            ratio=0.9,
                        ),
                    )
                    self.groupbox_manager.add_widget(
                        parent_id=f"{typ} 物件",
                        widget_id=f"{typ} 分隔線2",
                        widget=qt.QtLineCSWidget(),
                    )
                    _w = qt.QtTextLineCSWidget(
                        title=f"核實設備",
                        text=[
                            tool.String.list_to_string(
                                tool.XML.query_elems_attrs(
                                    store.collect_data.get("type_of")
                                    .get("okay")
                                    .get(typ),
                                    attr="name",
                                )
                            ),
                            len(
                                store.collect_data.get("type_of").get("okay").get(typ)
                            ).__str__(),
                        ],
                        readonly=True,
                        ratio=0.9,
                    )
                    if len(store.collect_data.get("type_of").get("okay").get(typ)) > 0:
                        _w.set_status(qt.QtLineEditStatus.Success)
                    self.groupbox_manager.add_widget(
                        parent_id=f"{typ} 物件",
                        widget_id=f"{typ} 核實設備",
                        widget=_w,
                    )
                    _w = qt.QtTextLineCSWidget(
                        title=f"無效設備",
                        text=[
                            tool.String.list_to_string(
                                tool.XML.query_elems_attrs(
                                    store.collect_data.get("type_of")
                                    .get("none")
                                    .get(typ),
                                    attr="name",
                                )
                            ),
                            len(
                                store.collect_data.get("type_of").get("none").get(typ)
                            ).__str__(),
                        ],
                        readonly=True,
                        ratio=0.9,
                    )
                    if len(store.collect_data.get("type_of").get("none").get(typ)) > 0:
                        _w.set_status(qt.QtLineEditStatus.Error)
                    self.groupbox_manager.add_widget(
                        parent_id=f"{typ} 物件",
                        widget_id=f"{typ} 無效設備",
                        widget=_w,
                    )
                    _w = qt.QtTextLineCSWidget(
                        title=f"暫代設備",
                        text=[
                            tool.String.list_to_string(
                                tool.XML.query_elems_attrs(
                                    store.collect_data.get("type_of")
                                    .get("temp")
                                    .get(typ),
                                    attr="name",
                                )
                            ),
                            len(
                                store.collect_data.get("type_of").get("temp").get(typ)
                            ).__str__(),
                        ],
                        readonly=True,
                        ratio=0.9,
                    )
                    if len(store.collect_data.get("type_of").get("temp").get(typ)) > 0:
                        _w.set_status(qt.QtLineEditStatus.Warning)
                    self.groupbox_manager.add_widget(
                        parent_id=f"{typ} 物件",
                        widget_id=f"{typ} 暫代設備",
                        widget=_w,
                    )
                    self.groupbox_manager.add_widget(
                        parent_id=f"{typ} 物件",
                        widget_id=f"{typ} 分隔線3",
                        widget=qt.QtLineCSWidget(),
                    )
                    _w = qt.QtTextLineCSWidget(
                        title=f"重複設備",
                        text=[
                            tool.String.list_to_string(
                                tool.XML.query_elems_attrs(
                                    store.collect_data.get("type_of")
                                    .get("dupe")
                                    .get(typ),
                                    attr="name",
                                )
                            ),
                            len(
                                store.collect_data.get("type_of").get("dupe").get(typ)
                            ).__str__(),
                        ],
                        readonly=True,
                        ratio=0.9,
                    )
                    if len(store.collect_data.get("type_of").get("dupe").get(typ)) > 0:
                        _w.set_status(qt.QtLineEditStatus.Info)
                    self.groupbox_manager.add_widget(
                        parent_id=f"{typ} 物件",
                        widget_id=f"{typ} 重複設備",
                        widget=_w,
                    )

                    if len(store.collect_data.get("type_of").get("none").get(typ)) > 0:
                        self.groupbox_manager.add_widget(
                            parent_id=f"{typ} 物件",
                            widget_id=f"{typ} 無效設備提示",
                            widget=qt.QtInfoBoxCSWidget(
                                text="發現無效設備，請嘗試修正點位檔案（.xml）再重試一次，如有需要請連繫相關人員。",
                                status=qt.QtInfoBoxStatus.Error,
                            ),
                        )
                    if len(store.collect_data.get("type_of").get("temp").get(typ)) > 0:
                        self.groupbox_manager.add_widget(
                            parent_id=f"{typ} 物件",
                            widget_id=f"{typ} 暫代設備提示",
                            widget=qt.QtInfoBoxCSWidget(
                                text="發現暫代設備，此類設備可能已準備進行模型置換，但還沒有被賦予實際模型路徑。",
                                status=qt.QtInfoBoxStatus.Warning,
                            ),
                        )
                    if len(store.collect_data.get("type_of").get("dupe").get(typ)) > 0:
                        self.groupbox_manager.add_widget(
                            parent_id=f"{typ} 物件",
                            widget_id=f"{typ} 重複設備提示",
                            widget=qt.QtInfoBoxCSWidget(
                                text="發現重複設備，請檢查重複的設備是否有必要修正。",
                                status=qt.QtInfoBoxStatus.Info,
                            ),
                        )
                    self.groupbox_manager.add_widget(
                        parent_id=f"{typ} 物件",
                        widget_id=f"{typ} OCMS提示",
                        widget=qt.QtInfoBoxCSWidget(
                            text="自 OCMS2.0 開始，由於部分屬性合併，＂各類 bundle＂、＂暫代設備＂將會被拿掉。",
                            status=qt.QtInfoBoxStatus.Help,
                        ),
                    )
                elif store.product_type == "OCMS2_0":
                    self.groupbox_manager.add_widget(
                        parent_id=f"點位物件統計",
                        widget_id=f"{typ} Model",
                        widget=qt.QtTextLineCSWidget(
                            title=f"{typ} Model",
                            text=[
                                tool.String.list_to_string(
                                    store.collect_data.get("type_of")
                                    .get("model")
                                    .get(typ)
                                ),
                                len(
                                    store.collect_data.get("type_of")
                                    .get("model")
                                    .get(typ)
                                ).__str__(),
                            ],
                            readonly=True,
                            ratio=0.9,
                        ),
                    )
                    self.groupbox_manager.add_widget(
                        parent_id=f"{typ} 物件",
                        widget_id=f"{typ} 數量",
                        widget=qt.QtTextLineCSWidget(
                            title=f"{typ} 數量",
                            text=[
                                tool.String.list_to_string(
                                    tool.XML.query_elems_attrs(
                                        store.collect_data.get("type_of")
                                        .get("element")
                                        .get(typ),
                                        attr="name",
                                    )
                                ),
                                len(
                                    store.collect_data.get("type_of")
                                    .get("element")
                                    .get(typ)
                                ).__str__(),
                            ],
                            readonly=True,
                            ratio=0.9,
                        ),
                    )
                    self.groupbox_manager.add_widget(
                        parent_id=f"{typ} 物件",
                        widget_id=f"{typ} 分隔線2",
                        widget=qt.QtLineCSWidget(),
                    )
                    _w = qt.QtTextLineCSWidget(
                        title=f"核實設備",
                        text=[
                            tool.String.list_to_string(
                                tool.XML.query_elems_attrs(
                                    store.collect_data.get("type_of")
                                    .get("okay")
                                    .get(typ),
                                    attr="name",
                                )
                            ),
                            len(
                                store.collect_data.get("type_of").get("okay").get(typ)
                            ).__str__(),
                        ],
                        readonly=True,
                        ratio=0.9,
                    )
                    if len(store.collect_data.get("type_of").get("okay").get(typ)) > 0:
                        _w.set_status(qt.QtLineEditStatus.Success)
                    self.groupbox_manager.add_widget(
                        parent_id=f"{typ} 物件",
                        widget_id=f"{typ} 核實設備",
                        widget=_w,
                    )
                    _w = qt.QtTextLineCSWidget(
                        title=f"無效設備",
                        text=[
                            tool.String.list_to_string(
                                tool.XML.query_elems_attrs(
                                    store.collect_data.get("type_of")
                                    .get("none")
                                    .get(typ),
                                    attr="name",
                                )
                            ),
                            len(
                                store.collect_data.get("type_of").get("none").get(typ)
                            ).__str__(),
                        ],
                        readonly=True,
                        ratio=0.9,
                    )
                    if len(store.collect_data.get("type_of").get("none").get(typ)) > 0:
                        _w.set_status(qt.QtLineEditStatus.Error)
                    self.groupbox_manager.add_widget(
                        parent_id=f"{typ} 物件",
                        widget_id=f"{typ} 無效設備",
                        widget=_w,
                    )
                    self.groupbox_manager.add_widget(
                        parent_id=f"{typ} 物件",
                        widget_id=f"{typ} 分隔線3",
                        widget=qt.QtLineCSWidget(),
                    )
                    _w = qt.QtTextLineCSWidget(
                        title=f"重複設備",
                        text=[
                            tool.String.list_to_string(
                                tool.XML.query_elems_attrs(
                                    store.collect_data.get("type_of")
                                    .get("dupe")
                                    .get(typ),
                                    attr="name",
                                )
                            ),
                            len(
                                store.collect_data.get("type_of").get("dupe").get(typ)
                            ).__str__(),
                        ],
                        readonly=True,
                        ratio=0.9,
                    )
                    if len(store.collect_data.get("type_of").get("dupe").get(typ)) > 0:
                        _w.set_status(qt.QtLineEditStatus.Info)
                    self.groupbox_manager.add_widget(
                        parent_id=f"{typ} 物件",
                        widget_id=f"{typ} 重複設備",
                        widget=_w,
                    )
                    if len(store.collect_data.get("type_of").get("none").get(typ)) > 0:
                        self.groupbox_manager.add_widget(
                            parent_id=f"{typ} 物件",
                            widget_id=f"{typ} 無效設備提示",
                            widget=qt.QtInfoBoxCSWidget(
                                text="發現無效設備，請嘗試修正點位檔案（.xml）再重試一次，如有需要請連繫相關人員。",
                                status=qt.QtInfoBoxStatus.Error,
                            ),
                        )

                    if len(store.collect_data.get("type_of").get("dupe").get(typ)) > 0:
                        self.groupbox_manager.add_widget(
                            parent_id=f"{typ} 物件",
                            widget_id=f"{typ} 重複設備提示",
                            widget=qt.QtInfoBoxCSWidget(
                                text="發現重複設備，請檢查重複的設備是否有必要修正。",
                                status=qt.QtInfoBoxStatus.Info,
                            ),
                        )
        helper.Logger.info(__name__, "Finished constructing types of widgets")
        import ocmseditor.oe.ui as global_ui

        helper.Logger.info(__name__, "Starting to update top level ui")
        global_ui.update_top_level_ui()
        # helper.Log.info(__name__, "Starting to toggle frame expand by widget")
        # global_ui.toggle_frame_expand_by_widget(self)
        helper.Logger.info(__name__, "Finished constructing widgets")
