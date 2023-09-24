import ocmseditor.oe.qt as qt
import ocmseditor.tool as tool
import ocmseditor.oe.helper as helper
import ocmseditor.oe.data.const as const

from . import operator


class SetProjectDirectoryCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.set_text("設定專案")

        self.scrollarea = qt.QtScrollareaCSWidget()

        self.project_dir_box = qt.QtGroupHBoxCSWidget()
        self.project_dir_box.set_text("專案路徑")

        self.fetch_btn = qt.QtButtonCSWidget()
        self.fetch_btn.set_width(4)
        self.fetch_btn.set_height(16)
        self.fetch_btn.set_tooltip("Fetch")

        self.project_dir_txt = qt.QtTextLineCSWidget()
        self.project_dir_txt.set_text("")
        self.project_dir_txt.lineedit.setReadOnly(True)

        self.browse_btn = qt.QtButtonCSWidget()
        self.browse_btn.set_icon("open_folder.png")
        self.browse_btn.set_text("")
        self.browse_btn.set_height(32)

        self.fetch_btn.clicked.connect(lambda: operator.op_fetch_project_path(self))
        self.browse_btn.clicked.connect(lambda: operator.op_browser_project_path(self))

        self.project_dir_box.layout.addWidget(self.fetch_btn)
        self.project_dir_box.layout.addWidget(self.project_dir_txt)
        self.project_dir_box.layout.addWidget(self.browse_btn)

        self.scrollarea.layout.addWidget(self.project_dir_box)

        self.frame_layout.addWidget(self.scrollarea)

        self._validate()

    def _preconstruct(self, project_dir):
        tool.Widget.set_text(self.project_dir_txt.lineedit, project_dir)

    def _validate(self):
        helper.Logger.info(__name__, "Validating project directory")
        # Operator: Validate
        project_path = tool.Registry.get_reg(const.REG_PROJ_PATH)
        self._preconstruct(project_path)
