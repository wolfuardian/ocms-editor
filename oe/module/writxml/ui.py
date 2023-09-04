import logging

import oe.tools as tools

from oe.utils import qt

from . import operator, store


def _hex(h):
    return "#" + h


class WriteXMLCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None, text="匯出XML檔案"):
        super().__init__(parent, text)

        self.scrollarea = qt.QtScrollareaCSWidget()
        self.scrollarea.setSizePolicy(
            qt.QtWidgets.QSizePolicy.Expanding, qt.QtWidgets.QSizePolicy.Expanding
        )

        self.dynamic_box = store.DynamicUIGroupManager()

        self.box_writexml = qt.QtGroupHBoxCSWidget(text="XML路徑")
        self.txt_writexml_path = qt.QtTextLineCSWidget(text="")
        self.txt_writexml_path.lineedit.setReadOnly(True)
        self.btn_writexml = qt.QtButtonCSWidget(
            icon="export_file.png",
            text="  匯出XML",
            height=32,
            status=qt.QtButtonStatus.Invert,
        )
        self.btn_browser_explorer = qt.QtButtonCSWidget(
            icon="folder.png",
            height=32,
        )
        self.box_writexml.layout.addWidget(self.txt_writexml_path)
        self.box_writexml.layout.addWidget(self.btn_writexml)
        self.box_writexml.layout.addWidget(self.btn_browser_explorer)
        self.scrollarea.layout.addWidget(self.box_writexml)
        self.scrollarea.layout.addWidget(self.dynamic_box.groupbox)

        self.btn_writexml.clicked.connect(
            lambda: operator.op_write_xml(self)
        )
        self.btn_browser_explorer.clicked.connect(
            lambda: operator.op_browser_explorer(self)
        )
        self.frame_layout.addWidget(self.scrollarea)
        self._browser_path = ""
