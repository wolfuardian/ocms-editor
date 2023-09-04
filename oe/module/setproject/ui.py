import oe.tools as tools

from oe.utils import qt

from . import operator
from oe.refer import Registry as reg_


def _hex(h):
    return "#" + h


class SetProjectDirectoryCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None, text="設定專案目錄"):
        super().__init__(parent, text)

        self.scrollarea = qt.QtScrollareaCSWidget()

        # Construct
        # <專案目錄>
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
        self.btn_browser_proj_dir = qt.QtButtonCSWidget(
            icon="open_folder.png", text="", height=32
        )
        self.btn_browser_proj_dir.set_force_visible(False)

        # Connect function
        # <專案目錄>
        self.btn_init_proj_dir.clicked.connect(
            lambda: operator.op_initialize_project_dir(self)
        )
        self.btn_browser_proj_dir.clicked.connect(
            lambda: operator.op_browser_project_dir(self)
        )

        # Assembly UI
        self.box_proj_dir.layout.addWidget(self.txt_proj_dir)
        self.box_proj_dir.layout.addWidget(self.btn_init_proj_dir)
        self.box_proj_dir.layout.addWidget(self.btn_browser_proj_dir)
        self.scrollarea.layout.addWidget(self.box_proj_dir)

        self.frame_layout.addWidget(self.scrollarea)

        # Validate
        # self.validate_init_proj_dir()

    def validate_init_proj_dir(self):
        tools.Logging.set_project_logger().info(
            "Validating initialize project directory"
        )
        _default_dir = tools.Registry.get_value(
            reg_.REG_KEY, reg_.REG_SUB, reg_.REG_PROJ_DIR, ""
        )
        if _default_dir != "":
            operator.op_initialize_project_dir(self)
