from oe.utils import qt

from . import operator


class SetProjectDirectoryCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.set_text("設定專案目錄")

        self.scrollarea = qt.QtScrollareaCSWidget()
        self.scrollarea.setSizePolicy(
            qt.QtWidgets.QSizePolicy.Expanding, qt.QtWidgets.QSizePolicy.Expanding
        )

        self.project_dir_box = qt.QtGroupHBoxCSWidget()
        self.project_dir_box.set_text("專案目錄")

        self.project_dir_txt = qt.QtTextLineCSWidget()
        self.project_dir_txt.set_text("")
        self.project_dir_txt.lineedit.setReadOnly(True)
        self.project_dir_txt.set_force_visible(False)

        self.init_project_dir_btn = qt.QtButtonCSWidget()
        self.init_project_dir_btn.set_icon("open_folder.png")
        self.init_project_dir_btn.set_text("  初始化")
        self.init_project_dir_btn.set_height(32)

        self.browse_project_dir_btn = qt.QtButtonCSWidget()
        self.browse_project_dir_btn.set_icon("open_folder.png")
        self.browse_project_dir_btn.set_text("")
        self.browse_project_dir_btn.set_height(32)
        self.browse_project_dir_btn.set_force_visible(False)

        self.init_project_dir_btn.clicked.connect(
            lambda: operator.op_init_project_dir(self)
        )
        self.browse_project_dir_btn.clicked.connect(
            lambda: operator.op_browser_project_dir(self)
        )

        self.project_dir_box.layout.addWidget(self.project_dir_txt)
        self.project_dir_box.layout.addWidget(self.init_project_dir_btn)
        self.project_dir_box.layout.addWidget(self.browse_project_dir_btn)

        self.scrollarea.layout.addWidget(self.project_dir_box)

        self.frame_layout.addWidget(self.scrollarea)

        operator.validate_project_dir(self)
