from ocmseditor.oe import ocms

from ocmseditor.oe import qt

from . import operator


class ImportResourcesCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.set_text("匯入模型資源")

        self.scrollarea = qt.QtScrollareaCSWidget()
        self.scrollarea.setSizePolicy(
            qt.QtWidgets.QSizePolicy.Expanding, qt.QtWidgets.QSizePolicy.Expanding
        )

        self.groupvbox = ocms.QtGroupVBoxStore()

        self.res_import_box = qt.QtGroupHBoxCSWidget()
        self.res_import_box.set_text("模型資源")

        self.import_res_btn = qt.QtButtonCSWidget()
        self.import_res_btn.set_icon("open_file.png")
        self.import_res_btn.set_text("  匯入資源")
        self.import_res_btn.set_height(32)

        self.import_res_btn.clicked.connect(lambda: operator.op_import_resources(self))

        self.res_import_box.layout.addWidget(self.import_res_btn)

        self.scrollarea.layout.addWidget(self.res_import_box)
        self.scrollarea.layout.addWidget(self.groupvbox.get_groupbox())

        self.frame_layout.addWidget(self.scrollarea)
