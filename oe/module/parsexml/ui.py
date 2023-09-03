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

        self.dynamic_box = store.DynamicUIGroupManager()

        self.box_xml_path = qt.QtGroupHBoxCSWidget(text="XML路徑")
        self.txt_xml_path = qt.QtTextLineCSWidget(text="")
        self.txt_xml_path.lineedit.setReadOnly(True)
        self.txt_xml_path.set_force_visible(False)
        self.btn_initialize = qt.QtButtonCSWidget(
            icon="open_file.png",
            text="  初始化",
            height=32,
            status=qt.QtButtonStatus.Invert,
        )
        self.btn_browser = qt.QtButtonCSWidget(
            icon="open_file.png", text="", height=32
        )
        self.btn_browser.set_force_visible(False)

        self.box_xml_path.layout.addWidget(self.txt_xml_path)
        self.box_xml_path.layout.addWidget(self.btn_initialize)
        self.box_xml_path.layout.addWidget(self.btn_browser)
        self.scrollarea.layout.addWidget(self.box_xml_path)
        self.scrollarea.layout.addWidget(self.dynamic_box.groupbox)

        self.btn_initialize.clicked.connect(
            lambda: operator.op_initialize_xml_path(self)
        )
        self.btn_browser.clicked.connect(lambda: operator.op_browser_xml_path(self))

        self.frame_layout.addWidget(self.scrollarea)
