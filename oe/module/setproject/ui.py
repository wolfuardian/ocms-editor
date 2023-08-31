from PySide2 import QtWidgets
from oe.utils import qt

# from . import operator, prop, store


class SetProjectDirectoryCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_text("專案目錄")

        # <editor-fold desc="CODE_BLOCK: Initialize">
        widget = qt.QtDefaultCSWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(6)
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Create Widget">
        scrollarea = qt.QtScrollareaCSWidget(margin=(12, 12, 12, 12), spacing=12)
        box_sel_mats = qt.QtGroupVBoxCSWidget(
            text="選取材質球", margin=(6, 24, 6, 6), spacing=6
        )
        box_sel_mats_in_scene = qt.QtGroupHBoxCSWidget(
            text="在場景中", margin=(6, 24, 6, 6), spacing=6
        )
        btn_sel_mats_in_scene = qt.QtButtonCSWidget(text="選取所有", height=24)
        btn_cancel_sel_mats = qt.QtButtonCSWidget(
            text="", icon="783_multiply_delete.svg", width=24, height=24
        )
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Set Status">
        # box_sel_mats_in_scene.set_status(qt.QtGroupBoxStatus.Borderless_Invert)
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Tooltip">
        # btn_sel_mats_in_scene.setToolTip("❓ 選取場景中所有材質球\n除了lambert1、standardSurface1、particleCloud1")
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Connect Action">
        # btn_sel_mats_in_scene.clicked.connect(operator.op_sel_mats)
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Assembly Widget">
        box_sel_mats_in_scene.layout.addWidget(btn_sel_mats_in_scene)
        box_sel_mats_in_scene.layout.addWidget(btn_cancel_sel_mats)
        scrollarea.layout.addWidget(box_sel_mats)
        layout.addWidget(scrollarea)
        widget.setLayout(layout)
        self.frame_layout.addWidget(widget)
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Expose Variable">
        self.layout = layout
        self.widget = widget
        # </editor-fold>
