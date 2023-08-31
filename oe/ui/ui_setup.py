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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Create Widget">
        menubar = qt.QtWidgets.QMenuBar()
        menubar.setToolTip("💡 此功能列僅供開發者使用")
        act_reset = qt.QtWidgets.QAction("R")
        act_expand_all = qt.QtWidgets.QAction("😎")

        tab = qt.QtTabCSWidget()
        tab_load = qt.QtTabItemCSWidget()
        tab_edit = qt.QtTabItemCSWidget()
        tab_save = qt.QtTabItemCSWidget()

        frame_set_project_directory_widget = module.SetProjectDirectoryCSWidget()

        tab_load.layout.addWidget(frame_set_project_directory_widget)
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Assembly Widget">
        tab.addTab(tab_load, "讀取")
        tab.addTab(tab_edit, "編輯")
        tab.addTab(tab_save, "儲存")
        layout.addWidget(tab)
        menubar.addAction(act_reset)
        menubar.addAction(act_expand_all)
        self.setLayout(layout)
        self.layout().setMenuBar(menubar)
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Expose Variable">
        self.layout = layout
        self.bar = menubar
        self.tab = tab
        self.tab_tool = tab_load
        self.act_reset = act_reset
        self.act_expand_all = act_expand_all

        self.frame_widgets = [
            frame_set_project_directory_widget,
        ]
        # </editor-fold>
