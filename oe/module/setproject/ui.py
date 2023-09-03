from oe.utils import qt

from . import operator


def _hex(h):
    return "#" + h


class SetProjectDirectoryCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None, text="設定專案目錄"):
        super().__init__(parent, text)

        # <editor-fold desc="CODE_BLOCK: Create Widget">
        scrollarea = qt.QtScrollareaCSWidget()

        box_proj_dir = qt.QtGroupHBoxCSWidget(text="專案目錄")
        txt_proj_dir = qt.QtTextLineCSWidget(text="")
        txt_proj_dir.lineedit.setReadOnly(True)
        txt_proj_dir.set_force_visible(False)
        btn_init_proj_dir = qt.QtButtonCSWidget(
            icon="open_folder.png",
            text="  初始化",
            height=32,
            status=qt.QtButtonStatus.Invert,
        )
        ui_btn_browser_proj_dir = qt.QtButtonCSWidget(
            icon="open_folder.png", text="", height=32
        )
        ui_btn_browser_proj_dir.set_force_visible(False)

        box_res_src_dir = qt.QtGroupHBoxCSWidget(text="來源模型檔目錄")
        txt_res_src_dir = qt.QtTextLineCSWidget(text="")
        txt_res_src_dir.lineedit.setReadOnly(True)
        txt_res_src_dir.set_force_visible(False)
        btn_init_res_src_dir = qt.QtButtonCSWidget(
            icon="open_folder.png",
            text="  初始化",
            height=32,
            status=qt.QtButtonStatus.Invert,
        )
        ui_btn_browser_res_src_dir = qt.QtButtonCSWidget(
            icon="open_folder.png", text="", height=32
        )
        ui_btn_browser_res_src_dir.set_force_visible(False)

        box_res_tar_dir = qt.QtGroupHBoxCSWidget(text="目標模型檔目錄")
        txt_res_tar_dir = qt.QtTextLineCSWidget(text="")
        txt_res_tar_dir.lineedit.setReadOnly(True)
        txt_res_tar_dir.set_force_visible(False)
        btn_init_res_tar_dir = qt.QtButtonCSWidget(
            icon="open_folder.png",
            text="  初始化",
            height=32,
            status=qt.QtButtonStatus.Invert,
        )
        ui_btn_browser_res_tar_dir = qt.QtButtonCSWidget(
            icon="open_folder.png", text="", height=32
        )
        ui_btn_browser_res_tar_dir.set_force_visible(False)
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Tooltip">
        btn_init_proj_dir.setToolTip("💡 初始化 專案目錄 路徑")
        ui_btn_browser_proj_dir.setToolTip("💡 瀏覽並選取 專案目錄 路徑")
        btn_init_res_src_dir.setToolTip("💡 初始化  來源模型檔目錄 路徑")
        ui_btn_browser_res_src_dir.setToolTip("💡 瀏覽並選取 來源模型檔目錄 路徑")
        btn_init_res_tar_dir.setToolTip("💡 初始化  目標模型檔目錄 路徑")
        ui_btn_browser_res_tar_dir.setToolTip("💡 瀏覽並選取 目標模型檔目錄 路徑")
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Connect Action">
        btn_init_proj_dir.clicked.connect(
            lambda: operator.op_initialize_project_dir(
                {
                    "btn_init_proj_dir": btn_init_proj_dir,
                    "ui_btn_browser_proj_dir": ui_btn_browser_proj_dir,
                    "txt_proj_dir": txt_proj_dir,
                }
            )
        )
        ui_btn_browser_proj_dir.clicked.connect(
            lambda: operator.op_browser_project_dir(
                {
                    "ui_btn_browser_proj_dir": ui_btn_browser_proj_dir,
                    "btn_init_proj_dir": btn_init_proj_dir,
                    "txt_proj_dir": txt_proj_dir,
                }
            )
        )
        btn_init_res_src_dir.clicked.connect(
            lambda: operator.op_initialize_resources_source_dir(
                {
                    "btn_init_res_src_dir": btn_init_res_src_dir,
                    "ui_btn_browser_res_src_dir": ui_btn_browser_res_src_dir,
                    "txt_res_src_dir": txt_res_src_dir,
                }
            )
        )
        ui_btn_browser_res_src_dir.clicked.connect(
            lambda: operator.op_browser_resources_source_dir(
                {
                    "ui_btn_browser_res_src_dir": ui_btn_browser_res_src_dir,
                    "btn_init_res_src_dir": btn_init_res_src_dir,
                    "txt_res_src_dir": txt_res_src_dir,
                }
            )
        )
        btn_init_res_tar_dir.clicked.connect(
            lambda: operator.op_initialize_resources_target_dir(
                {
                    "btn_init_res_tar_dir": btn_init_res_tar_dir,
                    "ui_btn_browser_res_tar_dir": ui_btn_browser_res_tar_dir,
                    "txt_res_tar_dir": txt_res_tar_dir,
                }
            )
        )
        ui_btn_browser_res_tar_dir.clicked.connect(
            lambda: operator.op_browser_resources_target_dir(
                {
                    "ui_btn_browser_res_tar_dir": ui_btn_browser_res_tar_dir,
                    "btn_init_res_tar_dir": btn_init_res_tar_dir,
                    "txt_res_tar_dir": txt_res_tar_dir,
                }
            )
        )

        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Assembly Widget">
        box_proj_dir.layout.addWidget(txt_proj_dir)
        box_proj_dir.layout.addWidget(btn_init_proj_dir)
        box_proj_dir.layout.addWidget(ui_btn_browser_proj_dir)
        box_res_src_dir.layout.addWidget(txt_res_src_dir)
        box_res_src_dir.layout.addWidget(btn_init_res_src_dir)
        box_res_src_dir.layout.addWidget(ui_btn_browser_res_src_dir)
        box_res_tar_dir.layout.addWidget(txt_res_tar_dir)
        box_res_tar_dir.layout.addWidget(btn_init_res_tar_dir)
        box_res_tar_dir.layout.addWidget(ui_btn_browser_res_tar_dir)
        scrollarea.layout.addWidget(box_proj_dir)
        scrollarea.layout.addWidget(box_res_src_dir)
        scrollarea.layout.addWidget(box_res_tar_dir)

        self.frame_layout.addWidget(scrollarea)

        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Expose Variable">
        # </editor-fold>
