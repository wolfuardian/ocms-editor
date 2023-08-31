from maya.app.general import mayaMixin
from oe.utils import qt

import oe.tools as tools
import oe.module as module
from version import version as ver


class Setup(
    mayaMixin.MayaQWidgetDockableMixin,
    mayaMixin.MayaQWidgetBaseMixin,
    qt.QtDefaultCSWidget,
):
    def __init__(self, parent=tools.Maya.get_main_window()):
        super(Setup, self).__init__(parent)

        self.setWindowTitle(ver)
        self.setMinimumWidth(360)

        # <editor-fold desc="CODE_BLOCK: Initialize">
        layout = qt.QtWidgets.QVBoxLayout()
        layout.setAlignment(qt.QtCore.Qt.AlignTop)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(0)
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Create Widget">
        bar = qt.QtWidgets.QMenuBar()
        action_reset = qt.QtWidgets.QAction("重新載入")
        tab = qt.QtTabCSWidget()
        tab_opt = qt.QtTabItemCSWidget()
        ui_set_pdir = module.SetProjectDirectoryCSWidget()
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Assembly Widget">
        tab_opt.layout.addWidget(ui_set_pdir)
        tab.addTab(tab_opt, "讀取")
        layout.addWidget(tab)
        bar.addAction(action_reset)
        self.setLayout(layout)
        self.layout().setMenuBar(bar)
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Expose Variable">
        self.layout = layout
        self.bar = bar
        self.tab = tab
        self.tab_tool = tab_opt
        self.action_reset = action_reset
        # </editor-fold>
