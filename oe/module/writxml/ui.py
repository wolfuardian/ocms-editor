import oe.storage as storage

from oe.utils import qt

from . import operator, store


class WriteXMLCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.set_text("匯出XML檔案")

        self.scrollarea = qt.QtScrollareaCSWidget()
        self.scrollarea.setSizePolicy(
            qt.QtWidgets.QSizePolicy.Expanding, qt.QtWidgets.QSizePolicy.Expanding
        )

        self.dynamic_ui = storage.DynamicUIGroupManager()

        self.xml_box = qt.QtGroupHBoxCSWidget()
        self.xml_box.set_text("XML路徑")

        self.xml_path_txt = qt.QtTextLineCSWidget()
        self.xml_path_txt.set_text("")
        self.xml_path_txt.lineedit.setReadOnly(True)

        self.write_xml_btn = qt.QtButtonCSWidget()
        self.write_xml_btn.set_icon("export_file.png")
        self.write_xml_btn.set_text("  匯出XML")
        self.write_xml_btn.set_height(32)

        self.browse_btn = qt.QtButtonCSWidget()
        self.browse_btn.set_icon("folder.png")
        self.browse_btn.set_height(32)

        self.write_xml_btn.clicked.connect(lambda: operator.op_write_xml(self))
        self.browse_btn.clicked.connect(lambda: operator.op_browser_explorer(self))

        self.xml_box.layout.addWidget(self.xml_path_txt)
        self.xml_box.layout.addWidget(self.write_xml_btn)
        self.xml_box.layout.addWidget(self.browse_btn)

        self.scrollarea.layout.addWidget(self.xml_box)
        self.scrollarea.layout.addWidget(self.dynamic_ui.groupbox)

        self.frame_layout.addWidget(self.scrollarea)
