import oe.storage as storage

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

        self.groupvbox = storage.QtGroupVBox()

        self.resource_dir_box = qt.QtGroupHBoxCSWidget()
        self.resource_dir_box.set_text("來源模型檔目錄")

        self.fetch_btn = qt.QtButtonCSWidget()
        self.fetch_btn.set_width(4)
        self.fetch_btn.set_height(16)
        self.fetch_btn.set_tooltip("Fetch️")

        self.resource_dir_txt = qt.QtTextLineCSWidget()
        self.resource_dir_txt.set_text("")
        self.resource_dir_txt.lineedit.setReadOnly(True)
        self.resource_dir_txt.set_force_visible(False)

        self.init_btn = qt.QtButtonCSWidget()
        self.init_btn.set_icon("open_folder.png")
        self.init_btn.set_text("  初始化")
        self.init_btn.set_height(32)

        self.parse_btn = qt.QtButtonCSWidget()
        self.parse_btn.set_icon(":/out_multDoubleLinear.png")
        self.parse_btn.set_text("  分析")
        self.parse_btn.set_width(80)
        self.parse_btn.set_height(32)
        self.parse_btn.set_force_visible(False)

        self.browse_btn = qt.QtButtonCSWidget()
        self.browse_btn.set_icon("open_folder.png")
        self.browse_btn.set_text("")
        self.browse_btn.set_height(32)
        self.browse_btn.set_force_visible(False)

        self.fetch_btn.clicked.connect(lambda: operator.op_fetch_res_dir(self))
        self.init_btn.clicked.connect(lambda: operator.op_init_res_dir(self))
        self.parse_btn.clicked.connect(lambda: operator.op_parse_resources(self))
        self.browse_btn.clicked.connect(lambda: operator.op_browser_resources_dir(self))

        self.resource_dir_box.layout.addWidget(self.fetch_btn)
        self.resource_dir_box.layout.addWidget(self.resource_dir_txt)
        self.resource_dir_box.layout.addWidget(self.init_btn)
        self.resource_dir_box.layout.addWidget(self.parse_btn)
        self.resource_dir_box.layout.addWidget(self.browse_btn)

        self.scrollarea.layout.addWidget(self.resource_dir_box)
        self.scrollarea.layout.addWidget(self.groupvbox.get_groupbox())

        self.frame_layout.addWidget(self.scrollarea)

        operator.validate_resources_dir(self)
