from oe.utils import qt

from . import operator


def _hex(h):
    return "#" + h


class SetProjectDirectoryCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None, text="設定專案目錄"):
        super().__init__(parent, text)

        self.scrollarea = qt.QtScrollareaCSWidget()

        self.box_proj_dir = qt.QtGroupHBoxCSWidget(text="專案目錄")
        self.txt_proj_dir = qt.QtTextLineCSWidget(text="")
        self.txt_proj_dir.lineedit.setReadOnly(True)
        self.txt_proj_dir.set_force_visible(False)
        self.btn_init_proj_dir = qt.QtButtonCSWidget(
            icon="open_folder.png",
            text="  初始化",
            height=32,
            status=qt.QtButtonStatus.Invert,
        )
        self.ui_btn_browser_proj_dir = qt.QtButtonCSWidget(
            icon="open_folder.png", text="", height=32
        )
        self.ui_btn_browser_proj_dir.set_force_visible(False)

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
        self.ui_btn_browser_res_src_dir = qt.QtButtonCSWidget(
            icon="open_folder.png", text="", height=32
        )
        self.ui_btn_browser_res_src_dir.set_force_visible(False)

        self.box_res_tar_dir = qt.QtGroupHBoxCSWidget(text="目標模型檔目錄")
        self.txt_res_tar_dir = qt.QtTextLineCSWidget(text="")
        self.txt_res_tar_dir.lineedit.setReadOnly(True)
        self.txt_res_tar_dir.set_force_visible(False)
        self.btn_init_res_tar_dir = qt.QtButtonCSWidget(
            icon="open_folder.png",
            text="  初始化",
            height=32,
            status=qt.QtButtonStatus.Invert,
        )
        self.ui_btn_browser_res_tar_dir = qt.QtButtonCSWidget(
            icon="open_folder.png", text="", height=32
        )
        self.ui_btn_browser_res_tar_dir.set_force_visible(False)

        self.btn_init_proj_dir.clicked.connect(
            lambda: operator.op_initialize_project_dir(self)
        )
        self.ui_btn_browser_proj_dir.clicked.connect(
            lambda: operator.op_browser_project_dir(self)
        )
        self.btn_init_res_src_dir.clicked.connect(
            lambda: operator.op_initialize_resources_source_dir(self)
        )
        self.ui_btn_browser_res_src_dir.clicked.connect(
            lambda: operator.op_browser_resources_source_dir(self)
        )
        self.btn_init_res_tar_dir.clicked.connect(
            lambda: operator.op_initialize_resources_target_dir(self)
        )
        self.ui_btn_browser_res_tar_dir.clicked.connect(
            lambda: operator.op_browser_resources_target_dir(self)
        )

        self.box_proj_dir.layout.addWidget(self.txt_proj_dir)
        self.box_proj_dir.layout.addWidget(self.btn_init_proj_dir)
        self.box_proj_dir.layout.addWidget(self.ui_btn_browser_proj_dir)
        self.box_res_src_dir.layout.addWidget(self.txt_res_src_dir)
        self.box_res_src_dir.layout.addWidget(self.btn_init_res_src_dir)
        self.box_res_src_dir.layout.addWidget(self.ui_btn_browser_res_src_dir)
        self.box_res_tar_dir.layout.addWidget(self.txt_res_tar_dir)
        self.box_res_tar_dir.layout.addWidget(self.btn_init_res_tar_dir)
        self.box_res_tar_dir.layout.addWidget(self.ui_btn_browser_res_tar_dir)
        self.scrollarea.layout.addWidget(self.box_proj_dir)
        self.scrollarea.layout.addWidget(self.box_res_src_dir)
        self.scrollarea.layout.addWidget(self.box_res_tar_dir)

        self.frame_layout.addWidget(self.scrollarea)
