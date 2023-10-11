from maya.app.general import mayaMixin

from ocmseditor.oe.utils.qt import (
    QtWidgets,
    QtCore,
    QtGui,
    QtDefaultCSWidget,
    QtTabCSWidget,
    get_main_window,
)

from ocmseditor.oe.constant import VERSION_PATH


def version():
    with open(VERSION_PATH, "r") as f:
        return f.read().strip()


class UIMain(
    mayaMixin.MayaQWidgetDockableMixin,
    mayaMixin.MayaQWidgetBaseMixin,
    QtDefaultCSWidget,
):
    def __init__(self, parent=get_main_window()):
        super(UIMain, self).__init__(parent)

        self.setWindowTitle(version())
        self.window_size_factor = 1.0

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        menubar = QtWidgets.QMenuBar()

        action_wheel_up = QtWidgets.QAction()
        action_wheel_down = QtWidgets.QAction()
        action_reset = QtWidgets.QAction()
        action_expand_all = QtWidgets.QAction()
        action_collapse_all = QtWidgets.QAction()
        action_resize_win = QtWidgets.QAction()
        action_sync_maya_operator = QtWidgets.QAction()
        action_sync_maya_operator_label = QtWidgets.QAction()

        action_reset.setIcon(QtGui.QIcon(":/reloadReference.png"))
        action_expand_all.setIcon(QtGui.QIcon(":/expandInfluenceList.png"))
        action_collapse_all.setIcon(QtGui.QIcon(":/retractInfluenceList.png"))
        action_resize_win.setIcon(QtGui.QIcon(":/nodeGrapherToggleView.png"))
        action_sync_maya_operator.setIcon(QtGui.QIcon(":/recording.png"))
        action_sync_maya_operator_label.setText("")
        action_sync_maya_operator_label.setEnabled(False)

        tab = QtTabCSWidget()
        # tab_load = QtTabItemCSWidget()
        # tab_res = QtTabItemCSWidget()
        # tab_edit = QtTabItemCSWidget()
        # tab_save = QtTabItemCSWidget()
        #
        # frame_set_project = module.SetProjectDirectoryCSWidget()
        # frame_parse_xml = module.ParseXMLCSWidget()
        # frame_parse_res = module.ParseResourceCSWidget()
        # frame_write_xml = module.WriteXMLCSWidget()
        # frame_tool_box = module.ToolBoxCSWidget()
        # frame_edit_attr = module.EditAttributeCSWidget()

        # tab_load.layout.addWidget(frame_set_project)
        # tab_load.layout.addWidget(frame_parse_xml)
        # tab_res.layout.addWidget(frame_parse_res)
        # tab_edit.layout.addWidget(frame_edit_attr)
        # tab_save.layout.addWidget(frame_write_xml)
        #
        # tab.addTab(tab_load, "   專案 / 初始化   ")
        # tab.addTab(tab_edit, "   編輯   ")
        # tab.addTab(tab_res, "   資源工具   ")
        # tab.addTab(tab_save, "   輸出   ")
        layout.addWidget(tab)
        # layout.addWidget(frame_tool_box)
        menubar.addAction(action_reset)

        self.set_wheel_up_event(action_wheel_up)
        self.set_wheel_down_event(action_wheel_down)
        menubar.addAction(action_expand_all)
        menubar.addAction(action_collapse_all)
        menubar.addAction(action_resize_win)
        menubar.addAction(action_sync_maya_operator)
        menubar.addAction(action_sync_maya_operator_label)
        self.setLayout(layout)
        self.layout().setMenuBar(menubar)

        self.layout = layout
        self.bar = menubar
        self.tab = tab
        # self.tab_tool = tab_load

        self.action_reset = action_reset
        self.action_wheel_up = action_wheel_up
        self.action_wheel_down = action_wheel_down
        self.action_expand_all = action_expand_all
        self.action_collapse_all = action_collapse_all
        self.action_resize_win = action_resize_win
        self.action_sync_maya_operator = action_sync_maya_operator
        self.action_sync_maya_operator_label = action_sync_maya_operator_label

        self.frame_widgets = [
            # frame_set_project,
            # frame_parse_xml,
            # frame_parse_res,
            # frame_write_xml,
        ]

        # ocms = tool.OCMS.get_ocms()
        # ocms.ui.context.setdefault("global", self)
        # ocms.ui.context.setdefault("frame_set_project", frame_set_project)
        # ocms.ui.context.setdefault("frame_parse_xml", frame_parse_xml)
        # ocms.ui.context.setdefault("frame_parse_res", frame_parse_res)
        # ocms.ui.context.setdefault("frame_write_xml", frame_write_xml)
        # ocms.ui.context.setdefault("frame_tool_box", frame_tool_box)
        # ocms.ui.context.setdefault("frame_edit_attr", frame_edit_attr)
        #
        # self.toggle_resize_win()

