import oe.storage as storage

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

        self.groupvbox = storage.QtGroupVBox()

        self.xml_path_box = qt.QtGroupHBoxCSWidget()
        self.xml_path_box.set_text("XML路徑")

        self.fetch_btn = qt.QtButtonCSWidget()
        self.fetch_btn.set_width(4)
        self.fetch_btn.set_height(16)
        self.fetch_btn.set_tooltip("Fetch")

        self.xml_path_txt = qt.QtTextLineCSWidget()
        self.xml_path_txt.set_text("")
        self.xml_path_txt.lineedit.setReadOnly(True)
        self.xml_path_txt.set_force_visible(False)

        self.init_btn = qt.QtButtonCSWidget()
        self.init_btn.set_icon("open_file.png")
        self.init_btn.set_text("  初始化")
        self.init_btn.set_height(32)

        self.parse_btn = qt.QtButtonCSWidget()
        self.parse_btn.set_icon(":/out_multDoubleLinear.png")
        self.parse_btn.set_text("  分析")
        self.parse_btn.set_width(80)
        self.parse_btn.set_height(32)
        self.parse_btn.set_force_visible(False)

        self.browse_btn = qt.QtButtonCSWidget()
        self.browse_btn.set_icon("open_folder.png")
        self.browse_btn.set_text("")
        self.browse_btn.set_height(32)
        self.browse_btn.set_force_visible(False)

        self.fetch_btn.clicked.connect(lambda: operator.op_fetch_xml_path(self))
        self.init_btn.clicked.connect(lambda: operator.op_init_xml_path(self))
        self.parse_btn.clicked.connect(lambda: operator.op_parse_xml(self))
        self.browse_btn.clicked.connect(lambda: operator.op_browser_xml_path(self))

        self.xml_path_box.layout.addWidget(self.fetch_btn)
        self.xml_path_box.layout.addWidget(self.xml_path_txt)
        self.xml_path_box.layout.addWidget(self.init_btn)
        self.xml_path_box.layout.addWidget(self.parse_btn)
        self.xml_path_box.layout.addWidget(self.browse_btn)
        self.scrollarea.layout.addWidget(self.xml_path_box)
        self.scrollarea.layout.addWidget(self.groupvbox.get_groupbox())

        self.frame_layout.addWidget(self.scrollarea)

        operator.validate_xml_path(self)
