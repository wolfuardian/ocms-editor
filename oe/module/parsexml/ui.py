from oe.utils import qt

from . import operator, store


class ParseXMLCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.set_text("核實XML")

        self.scrollarea = qt.QtScrollareaCSWidget()
        self.scrollarea.setSizePolicy(
            qt.QtWidgets.QSizePolicy.Expanding, qt.QtWidgets.QSizePolicy.Expanding
        )

        self.dynamic_ui = store.DynamicUIGroupManager()

        self.xml_path_box = qt.QtGroupHBoxCSWidget()
        self.xml_path_box.set_text("XML路徑")

        self.xml_path_text = qt.QtTextLineCSWidget()
        self.xml_path_text.set_text("")
        self.xml_path_text.lineedit.setReadOnly(True)
        self.xml_path_text.set_force_visible(False)

        self.init_btn = qt.QtButtonCSWidget()
        self.init_btn.set_icon("open_file.png")
        self.init_btn.set_text("  初始化")
        self.init_btn.set_height(32)

        self.browse_btn = qt.QtButtonCSWidget()
        self.browse_btn.set_icon("open_folder.png")
        self.browse_btn.set_text("")
        self.browse_btn.set_height(32)
        self.browse_btn.set_force_visible(False)

        self.xml_path_box.layout.addWidget(self.xml_path_text)
        self.xml_path_box.layout.addWidget(self.init_btn)
        self.xml_path_box.layout.addWidget(self.browse_btn)
        self.scrollarea.layout.addWidget(self.xml_path_box)
        self.scrollarea.layout.addWidget(self.dynamic_ui.groupbox)

        self.init_btn.clicked.connect(lambda: operator.op_init_xml_path(self))
        self.browse_btn.clicked.connect(lambda: operator.op_browser_xml_path(self))

        self.frame_layout.addWidget(self.scrollarea)
