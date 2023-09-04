import logging

import oe.tools as tools

from oe.utils import qt

from . import operator, store
from oe.refer import Registry as reg_


def _hex(h):
    return "#" + h


class ParseResourcesCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None, text="核實模型檔"):
        super().__init__(parent, text)

        self.scrollarea = qt.QtScrollareaCSWidget()
        self.scrollarea.setSizePolicy(
            qt.QtWidgets.QSizePolicy.Expanding,
            qt.QtWidgets.QSizePolicy.MinimumExpanding,
        )

        self.dynamic_box = store.DynamicUIGroupManager()

        self.box_res_dir = qt.QtGroupHBoxCSWidget(text="來源模型檔目錄")
        self.txt_res_dir = qt.QtTextLineCSWidget(text="")
        self.txt_res_dir.lineedit.setReadOnly(True)
        self.txt_res_dir.set_force_visible(False)
        self.btn_init_res_dir = qt.QtButtonCSWidget(
            icon="open_folder.png",
            text="  初始化",
            height=32,
            status=qt.QtButtonStatus.Invert,
        )
        self.btn_browser_res_dir = qt.QtButtonCSWidget(
            icon="open_folder.png", text="", height=32
        )
        self.btn_browser_res_dir.set_force_visible(False)

        self.box_res_dir.layout.addWidget(self.txt_res_dir)
        self.box_res_dir.layout.addWidget(self.btn_init_res_dir)
        self.box_res_dir.layout.addWidget(self.btn_browser_res_dir)
        self.scrollarea.layout.addWidget(self.box_res_dir)
        self.scrollarea.layout.addWidget(self.dynamic_box.groupbox)

        self.btn_init_res_dir.clicked.connect(
            lambda: operator.op_init_res_dir(self)
        )
        self.btn_browser_res_dir.clicked.connect(
            lambda: operator.op_browser_resources_source_dir(self)
        )

        self.frame_layout.addWidget(self.scrollarea)

        # Validate
        # self.validate_init_res_dir()

    def validate_init_res_dir(self):
        tools.Logging.parse_xml_logger().info(
            "Validating initialize resources directory"
        )
        _default_dir = tools.Registry.get_value(
            reg_.REG_KEY, reg_.REG_SUB, reg_.REG_RES_DIR, ""
        )
        if _default_dir != "":
            operator.op_init_res_dir(self)
