import logging

import oe.tools as tools

from oe.utils import qt

from . import operator, store


def _hex(h):
    return "#" + h


class ParseResourcesCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None, text="核實模型檔"):
        super().__init__(parent, text)

        self.scrollarea = qt.QtScrollareaCSWidget()
        self.scrollarea.setFixedHeight(600)
        # self.scrollarea.setSizePolicy(
        #     qt.QtWidgets.QSizePolicy.Expanding, qt.QtWidgets.QSizePolicy.MinimumExpanding
        # )

        self.dynamic_box = store.DynamicUIGroupManager()

        self.box_res_src_dir = qt.QtGroupHBoxCSWidget(text="來源模型檔目錄")
        self.txt_res_src_dir = qt.QtTextLineCSWidget(text="")
        self.txt_res_src_dir.lineedit.setReadOnly(True)
        self.txt_res_src_dir.set_force_visible(False)
        self.btn_init_res_src_dir = qt.QtButtonCSWidget(
            icon="open_folder.png",
            text="  初始化",
            height=32,
            status=qt.QtButtonStatus.Invert,
        )
        self.btn_browser_res_src_dir = qt.QtButtonCSWidget(
            icon="open_folder.png", text="", height=32
        )
        self.btn_browser_res_src_dir.set_force_visible(False)

        self.box_res_src_dir.layout.addWidget(self.txt_res_src_dir)
        self.box_res_src_dir.layout.addWidget(self.btn_init_res_src_dir)
        self.box_res_src_dir.layout.addWidget(self.btn_browser_res_src_dir)
        self.scrollarea.layout.addWidget(self.box_res_src_dir)
        self.scrollarea.layout.addWidget(self.dynamic_box.groupbox)

        self.btn_init_res_src_dir.clicked.connect(
            lambda: operator.op_initialize_resources_source_dir(self)
        )
        self.btn_browser_res_src_dir.clicked.connect(
            lambda: operator.op_browser_resources_source_dir(self)
        )

        self.frame_layout.addWidget(self.scrollarea)
