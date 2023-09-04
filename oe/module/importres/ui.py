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

        self.box_xml_path = qt.QtGroupHBoxCSWidget(text="模型資源")
        self.txt_xml_path = qt.QtTextLineCSWidget(text="")
        self.txt_xml_path.lineedit.setReadOnly(True)
        self.txt_xml_path.set_force_visible(False)
        self.btn_import_resources = qt.QtButtonCSWidget(
            icon="open_file.png",
            text="  匯入資源",
            height=32,
            status=qt.QtButtonStatus.Invert,
        )

        self.box_xml_path.layout.addWidget(self.txt_xml_path)
        self.box_xml_path.layout.addWidget(self.btn_import_resources)
        self.scrollarea.layout.addWidget(self.box_xml_path)
        self.scrollarea.layout.addWidget(self.dynamic_box.groupbox)

        self.btn_import_resources.clicked.connect(
            lambda: operator.op_import_resources(self)
        )
        self.frame_layout.addWidget(self.scrollarea)
