from maya.app.general import mayaMixin

import oe.tools as tools
import oe.module as module
import oe.storage as storage

from oe.utils import qt

from product import prod_id


class Setup(
    mayaMixin.MayaQWidgetDockableMixin,
    mayaMixin.MayaQWidgetBaseMixin,
    qt.QtDefaultCSWidget,
):
    def __init__(self, parent=tools.Maya.get_main_window()):
        super(Setup, self).__init__(parent)

        self.setWindowTitle(prod_id)
        self.window_size_factor = 1.0

        layout = qt.QtWidgets.QVBoxLayout()
        layout.setAlignment(qt.QtCore.Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        menubar = qt.QtWidgets.QMenuBar()
        menubar.setToolTip("💡 此功能列僅供開發者使用")

        action_wheel_up = qt.QtWidgets.QAction()
        action_wheel_down = qt.QtWidgets.QAction()
        action_reset = qt.QtWidgets.QAction()
        action_expand_all = qt.QtWidgets.QAction()
        action_collapse_all = qt.QtWidgets.QAction()
        action_resize_win = qt.QtWidgets.QAction()

        action_reset.setIcon(qt.QtGui.QIcon(":/reloadReference.png"))
        action_expand_all.setIcon(qt.QtGui.QIcon(":/expandInfluenceList.png"))
        action_collapse_all.setIcon(qt.QtGui.QIcon(":/retractInfluenceList.png"))
        action_resize_win.setIcon(qt.QtGui.QIcon(":/nodeGrapherToggleView.png"))

        tab = qt.QtTabCSWidget()
        tab_load = qt.QtTabItemCSWidget()
        tab_edit = qt.QtTabItemCSWidget()
        tab_save = qt.QtTabItemCSWidget()

        frame_set_project = module.SetProjectDirectoryCSWidget()
        frame_parse_xml = module.ParseXMLCSWidget()
        frame_parse_res = module.ParseResourcesCSWidget()
        frame_import_res = module.ImportResourcesCSWidget()
        frame_writexml = module.WriteXMLCSWidget()

        tab_load.layout.addWidget(frame_set_project)
        tab_load.layout.addWidget(frame_parse_xml)
        tab_load.layout.addWidget(frame_parse_res)
        tab_load.layout.addWidget(frame_import_res)
        tab_save.layout.addWidget(frame_writexml)

        tab.addTab(tab_load, "讀取")
        tab.addTab(tab_edit, "編輯")
        tab.addTab(tab_save, "儲存")
        layout.addWidget(tab)
        menubar.addAction(action_reset)

        self.set_wheel_up_event(action_wheel_up)
        self.set_wheel_down_event(action_wheel_down)
        menubar.addAction(action_expand_all)
        menubar.addAction(action_collapse_all)
        menubar.addAction(action_resize_win)
        self.setLayout(layout)
        self.layout().setMenuBar(menubar)

        self.layout = layout
        self.bar = menubar
        self.tab = tab
        self.tab_tool = tab_load

        self.action_reset = action_reset
        self.action_wheel_up = action_wheel_up
        self.action_wheel_down = action_wheel_down
        self.action_expand_all = action_expand_all
        self.action_collapse_all = action_collapse_all
        self.action_resize_win = action_resize_win

        self.frame_widgets = [
            frame_set_project,
            frame_parse_xml,
            frame_parse_res,
            frame_import_res,
            frame_writexml,
        ]

        storage.UIData.ui.setdefault("frame_set_project", frame_set_project)
        storage.UIData.ui.setdefault("frame_parse_xml", frame_parse_xml)
        storage.UIData.ui.setdefault("frame_parse_res", frame_parse_res)
        storage.UIData.ui.setdefault("frame_import_res", frame_import_res)
        storage.UIData.ui.setdefault("frame_writexml", frame_writexml)

        self.toggle_resize_win()
