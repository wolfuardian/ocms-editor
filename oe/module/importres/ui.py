import logging

import oe.tools as tools

from oe.utils import qt

from . import operator, store


def _hex(h):
    return "#" + h


class ImportResourcesCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None, text="匯入模型資源"):
        super().__init__(parent, text)

        self.scrollarea = qt.QtScrollareaCSWidget()
        self.scrollarea.setSizePolicy(
            qt.QtWidgets.QSizePolicy.Expanding, qt.QtWidgets.QSizePolicy.Expanding
        )

        self.dynamic_box = store.DynamicUIGroupManager()

        self.box_import_res = qt.QtGroupHBoxCSWidget(text="模型資源")
        self.btn_import_res = qt.QtButtonCSWidget(
            icon="open_file.png",
            text="  匯入資源",
            height=32,
            status=qt.QtButtonStatus.Invert,
        )
        self.box_import_res.layout.addWidget(self.btn_import_res)
        self.scrollarea.layout.addWidget(self.box_import_res)
        self.scrollarea.layout.addWidget(self.dynamic_box.groupbox)

        self.btn_import_res.clicked.connect(lambda: operator.op_import_resources(self))
        self.frame_layout.addWidget(self.scrollarea)
