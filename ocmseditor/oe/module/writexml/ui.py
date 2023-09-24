import ocmseditor.oe.qt as qt
import ocmseditor.tool as tool
import ocmseditor.oe.helper as helper
import ocmseditor.oe.data.const as const

from . import operator


class WriteXMLCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.set_text("匯出XML檔案")

        self.scrollarea = qt.QtScrollareaCSWidget()
        self.scrollarea.setSizePolicy(
            qt.QtWidgets.QSizePolicy.Expanding, qt.QtWidgets.QSizePolicy.Expanding
        )

        self.groupbox_manager = qt.QtGroupboxManager()

        self.xml_box = qt.QtGroupHBoxCSWidget()
        self.xml_box.set_text("XML路徑")

        self.fetch_btn = qt.QtButtonCSWidget()
        self.fetch_btn.set_width(4)
        self.fetch_btn.set_height(16)
        self.fetch_btn.set_tooltip("Fetch")

        self.xml_write_path_txt = qt.QtTextLineCSWidget()
        self.xml_write_path_txt.set_text("")
        self.xml_write_path_txt.lineedit.setReadOnly(True)

        self.write_btn = qt.QtButtonCSWidget()
        self.write_btn.set_icon("export_file.png")
        self.write_btn.set_text("  匯出XML")
        self.write_btn.set_height(32)

        self.browse_btn = qt.QtButtonCSWidget()
        self.browse_btn.set_icon("folder.png")
        self.browse_btn.set_height(32)

        self.fetch_btn.clicked.connect(
            lambda: operator.op_fetch_write_xml_filepath(self)
        )
        self.write_btn.clicked.connect(lambda: operator.op_write_xml(self))
        self.browse_btn.clicked.connect(
            lambda: operator.op_browser_write_xml_filepath(self)
        )

        self.xml_box.layout.addWidget(self.fetch_btn)
        self.xml_box.layout.addWidget(self.xml_write_path_txt)
        self.xml_box.layout.addWidget(self.write_btn)
        self.xml_box.layout.addWidget(self.browse_btn)

        self.scrollarea.layout.addWidget(self.xml_box)
        self.scrollarea.layout.addWidget(self.groupbox_manager.get_groupbox())

        self.frame_layout.addWidget(self.scrollarea)

        self._validate()

    def _destroy(self):
        self.groupbox_manager.clear_all()

    def _validate(self):
        xml_write_path = tool.Registry.get_reg(const.REG_XML_EXPORT_FILEPATH)
        if not tool.File.is_xml(xml_write_path):
            tool.Widget.disable(self.write_btn)
        else:
            tool.Widget.enable(self.write_btn)

        self._preconstruct(xml_write_path)

    def _preconstruct(self, xml_path):
        tool.Widget.set_text(self.xml_write_path_txt.lineedit, xml_path)

    def _construct(self):
        helper.Logger.info(__name__, "Constructing widgets")
        self.groupbox_manager.add_group(
            widget_id="匯出結果", widget=qt.QtGroupVBoxCSWidget(text="匯出結果")
        )
        self.groupbox_manager.add_widget(
            parent_id="匯出結果",
            widget_id="已完成匯出XML，點擊右側按鈕開啟檔案位置",
            widget=qt.QtInfoBoxCSWidget(
                text=f"已完成匯出XML，點擊右側按鈕開啟檔案位置。",
                status=qt.QtInfoBoxStatus.Success,
            ),
        )
        helper.Logger.info(__name__, "Completed constructing dynamic ui group manager")
