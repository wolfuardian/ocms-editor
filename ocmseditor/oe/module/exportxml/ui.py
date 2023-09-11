from ocmseditor.oe import qt
from ocmseditor.oe import ocms

from . import operator


class ExportXMLCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.set_text("匯出XML檔案")

        self.scrollarea = qt.QtScrollareaCSWidget()
        self.scrollarea.setSizePolicy(
            qt.QtWidgets.QSizePolicy.Expanding, qt.QtWidgets.QSizePolicy.Expanding
        )

        self.groupvbox = ocms.QtGroupVBoxStore()

        self.xml_box = qt.QtGroupHBoxCSWidget()
        self.xml_box.set_text("XML路徑")

        self.fetch_btn = qt.QtButtonCSWidget()
        self.fetch_btn.set_width(4)
        self.fetch_btn.set_height(16)
        self.fetch_btn.set_tooltip("Fetch")

        self.xml_export_path_txt = qt.QtTextLineCSWidget()
        self.xml_export_path_txt.set_text("")
        self.xml_export_path_txt.lineedit.setReadOnly(True)

        self.export_btn = qt.QtButtonCSWidget()
        self.export_btn.set_icon("export_file.png")
        self.export_btn.set_text("  匯出XML")
        self.export_btn.set_height(32)

        self.browse_btn = qt.QtButtonCSWidget()
        self.browse_btn.set_icon("folder.png")
        self.browse_btn.set_height(32)

        self.fetch_btn.clicked.connect(lambda: operator.op_fetch(self))
        self.export_btn.clicked.connect(lambda: operator.op_export_xml(self))
        self.browse_btn.clicked.connect(lambda: operator.op_browser(self))

        self.xml_box.layout.addWidget(self.fetch_btn)
        self.xml_box.layout.addWidget(self.xml_export_path_txt)
        self.xml_box.layout.addWidget(self.export_btn)
        self.xml_box.layout.addWidget(self.browse_btn)

        self.scrollarea.layout.addWidget(self.xml_box)
        self.scrollarea.layout.addWidget(self.groupvbox.get_groupbox())

        self.frame_layout.addWidget(self.scrollarea)

        operator.validate(self)