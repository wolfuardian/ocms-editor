from PySide2 import QtWidgets
from oe.utils import qt

# from . import operator, prop, store

def _hex(h):
    return "#" + h

class SetProjectDirectoryCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None, text="專案目錄"):
        super().__init__(parent, text)

        # <editor-fold desc="CODE_BLOCK: Initialize">
        widget = qt.QtDefaultCSWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Create Widget">
        scrollarea = qt.QtScrollareaCSWidget()

        gbox_p_dir = qt.QtGroupHBoxCSWidget(text="專案目錄")
        tl_p_dir = qt.QtTextLineCSWidget(text="", placeholder="> 專案目錄路徑")
        tl_p_dir.lineedit.setReadOnly(True)
        btn_p_dir = qt.QtButtonCSWidget(text="< 開啟")

        gbox_m_dir = qt.QtGroupHBoxCSWidget(text="模型檔目錄")
        tl_m_dir = qt.QtTextLineCSWidget(text="", placeholder="> 模型檔目錄路徑")
        tl_m_dir.lineedit.setReadOnly(True)
        btn_m_dir = qt.QtButtonCSWidget(text="< 開啟")
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Set Status">
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Tooltip">
        gbox_p_dir.setToolTip("💡 選取場景中所有材質球，除了lambert1、standardSurface1、particleCloud1")
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Connect Action">
        # btn_sel_mats_in_scene.clicked.connect(operator.op_sel_mats)
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Assembly Widget">
        gbox_p_dir.layout.addWidget(tl_p_dir)
        gbox_p_dir.layout.addWidget(btn_p_dir)
        gbox_m_dir.layout.addWidget(tl_m_dir)
        gbox_m_dir.layout.addWidget(btn_m_dir)
        scrollarea.layout.addWidget(gbox_p_dir)
        scrollarea.layout.addWidget(gbox_m_dir)
        layout.addWidget(scrollarea)
        widget.setLayout(layout)
        self.frame_layout.addWidget(widget)
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Expose Variable">
        self.layout = layout
        self.widget = widget
        # </editor-fold>
