from maya.app.general import mayaMixin

import oe.tools as tools
import oe.module as module
import oe.storage as storage

from oe.utils import qt

from product import prod_id as prod_id


class Setup(
    mayaMixin.MayaQWidgetDockableMixin,
    mayaMixin.MayaQWidgetBaseMixin,
    qt.QtDefaultCSWidget,
):
    def __init__(self, parent=tools.Maya.get_main_window()):
        super(Setup, self).__init__(parent)

        self.setWindowTitle(prod_id)
        # self.setSizePolicy(qt.QtWidgets.QSizePolicy.Expanding, qt.QtWidgets.QSizePolicy.Minimum)
        self.window_size_factor = 1.0

        # <editor-fold desc="CODE_BLOCK: Initialize">
        layout = qt.QtWidgets.QVBoxLayout()
        layout.setAlignment(qt.QtCore.Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Create Widget">
        menubar = qt.QtWidgets.QMenuBar()
        menubar.setToolTip("💡 此功能列僅供開發者使用")
        action_reset = qt.QtWidgets.QAction("R")
        action_expand_all = qt.QtWidgets.QAction("😎")
        action_resize_win = qt.QtWidgets.QAction("💻")

        tab = qt.QtTabCSWidget()
        tab_load = qt.QtTabItemCSWidget()
        tab_edit = qt.QtTabItemCSWidget()
        tab_save = qt.QtTabItemCSWidget()

        frame_set_project = module.SetProjectDirectoryCSWidget()
        frame_parse_xml = module.ParseXMLCSWidget()
        frame_parse_res = module.ParseResourcesCSWidget()
        frame_import_res = module.ImportResourcesCSWidget()
        frame_writexml = module.WriteXMLCSWidget()
        # frame_parse_res = module.ParseResourcesCSWidget()

        # frame_set_project.frame_btn.toggle = False
        # frame_parse_xml.frame_btn.toggle = False
        # frame_parse_res.frame_btn.toggle = False

        tab_load.layout.addWidget(frame_set_project)
        tab_load.layout.addWidget(frame_parse_xml)
        tab_load.layout.addWidget(frame_parse_res)
        tab_load.layout.addWidget(frame_import_res)
        tab_load.layout.addWidget(frame_writexml)
        # tab_load.layout.addWidget(frame_parse_res)
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Assembly Widget">
        tab.addTab(tab_load, "讀取")
        tab.addTab(tab_edit, "編輯")
        tab.addTab(tab_save, "儲存")
        layout.addWidget(tab)
        menubar.addAction(action_reset)
        menubar.addAction(action_expand_all)
        menubar.addAction(action_resize_win)
        self.setLayout(layout)
        self.layout().setMenuBar(menubar)
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Expose Variable">
        self.layout = layout
        self.bar = menubar
        self.tab = tab
        self.tab_tool = tab_load
        self.action_reset = action_reset
        self.action_expand_all = action_expand_all
        self.action_resize_win = action_resize_win

        self.frame_widgets = [
            frame_set_project,
            frame_parse_xml,
            frame_parse_res,
            frame_import_res,
            frame_writexml,
        ]

        storage.UIData.ui["frame_set_project"] = frame_set_project
        storage.UIData.ui["frame_parse_xml"] = frame_parse_xml
        storage.UIData.ui["frame_parse_res"] = frame_parse_res
        storage.UIData.ui["frame_import_res"] = frame_import_res
        storage.UIData.ui["frame_writexml"] = frame_writexml

        self.toggle_resize_win()

        # </editor-fold>
