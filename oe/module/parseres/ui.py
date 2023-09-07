from oe.utils import qt

from . import operator, store


class ParseResourcesCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.set_text("核實模型檔")

        self.scrollarea = qt.QtScrollareaCSWidget()
        self.scrollarea.setSizePolicy(
            qt.QtWidgets.QSizePolicy.Expanding,
            qt.QtWidgets.QSizePolicy.MinimumExpanding,
        )

        self.dynamic_ui = store.DynamicUIGroupManager()

        self.resource_dir_box = qt.QtGroupHBoxCSWidget()
        self.resource_dir_box.set_text("來源模型檔目錄")

        self.resource_dir_txt = qt.QtTextLineCSWidget()
        self.resource_dir_txt.set_text("")
        self.resource_dir_txt.lineedit.setReadOnly(True)
        self.resource_dir_txt.set_force_visible(False)

        self.init_resource_dir_btn = qt.QtButtonCSWidget()
        self.init_resource_dir_btn.set_icon("open_folder.png")
        self.init_resource_dir_btn.set_text("  初始化")
        self.init_resource_dir_btn.set_height(32)

        self.browse_resource_dir_btn = qt.QtButtonCSWidget()
        self.browse_resource_dir_btn.set_icon("open_folder.png")
        self.browse_resource_dir_btn.set_text("")
        self.browse_resource_dir_btn.set_height(32)
        self.browse_resource_dir_btn.set_force_visible(False)

        self.init_resource_dir_btn.clicked.connect(
            lambda: operator.op_init_res_dir(self)
        )
        self.browse_resource_dir_btn.clicked.connect(
            lambda: operator.op_browser_resources_source_dir(self)
        )

        self.resource_dir_box.layout.addWidget(self.resource_dir_txt)
        self.resource_dir_box.layout.addWidget(self.init_resource_dir_btn)
        self.resource_dir_box.layout.addWidget(self.browse_resource_dir_btn)

        self.scrollarea.layout.addWidget(self.resource_dir_box)
        self.scrollarea.layout.addWidget(self.dynamic_ui.groupbox)

        self.frame_layout.addWidget(self.scrollarea)
