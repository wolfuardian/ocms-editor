import logging

import oe.tools as tools

from oe.utils import qt

from . import operator, store


def _hex(h):
    return "#" + h


class ParseXMLCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None, text="核實XML"):
        super().__init__(parent, text)

        self.scrollarea = qt.QtScrollareaCSWidget()
        self.scrollarea.setSizePolicy(
            qt.QtWidgets.QSizePolicy.Expanding, qt.QtWidgets.QSizePolicy.Expanding
        )

        tools.Logging.gui_logger().setLevel(level=logging.INFO)

        self.dynamic_box = store.DynamicUIGroupManager()

        self.box_xml_path = qt.QtGroupHBoxCSWidget(text="XML路徑")
        self.ui_le_xml_path = qt.QtTextLineCSWidget(text="")
        self.ui_le_xml_path.lineedit.setReadOnly(True)
        self.ui_le_xml_path.set_force_visible(False)
        self.ui_btn_initialize = qt.QtButtonCSWidget(
            icon="open_file.png",
            text="  初始化",
            height=32,
            status=qt.QtButtonStatus.Invert,
        )
        self.ui_btn_browser = qt.QtButtonCSWidget(
            icon="open_file.png", text="", height=32
        )
        self.ui_btn_browser.set_force_visible(False)

        self.box_xml_path.layout.addWidget(self.ui_le_xml_path)
        self.box_xml_path.layout.addWidget(self.ui_btn_initialize)
        self.box_xml_path.layout.addWidget(self.ui_btn_browser)
        self.scrollarea.layout.addWidget(self.box_xml_path)
        self.scrollarea.layout.addWidget(self.dynamic_box.groupbox)

        self.ui_btn_initialize.clicked.connect(
            lambda: operator.op_initialize_xml_path(self)
        )
        self.ui_btn_browser.clicked.connect(lambda: operator.op_browser_xml_path(self))

        self.frame_layout.addWidget(self.scrollarea)
