from maya.app.general import mayaMixin

from ocmseditor.oe.module import (
    attribute,
    file,
    imports,
    log,
    manage,
    node,
    parse,
    scene,
    visualize,
)
from ocmseditor.oe.utils.qt import (
    QtWidgets,
    QtCore,
    QtGui,
    QtDefaultCSWidget,
    QtTabCSWidget,
    QtTabBarCSWidget,
    QtTabItemCSWidget,
    QtButtonCSWidget,
    get_main_window,
)
from ocmseditor.oe.utils.qt_stylesheet import QtStyle, QtButtonStyle
from ocmseditor.oe.repository import Repository
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

        self.setWindowTitle(version().split("-")[0])
        self.window_size_factor = 0

        self.__layout = QtWidgets.QVBoxLayout()
        self.__layout.setAlignment(QtCore.Qt.AlignTop)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)

        self.__menubar = QtWidgets.QMenuBar()

        self.action_wheel_up = QtWidgets.QAction()
        self.action_wheel_down = QtWidgets.QAction()
        self.action_reset = QtWidgets.QAction()
        self.action_expand_all = QtWidgets.QAction()
        self.action_collapse_all = QtWidgets.QAction()
        self.action_resize_win = QtWidgets.QAction()
        self.action_sync_maya_operator = QtWidgets.QAction()
        self.action_sync_maya_operator_label = QtWidgets.QAction()

        self.action_expand_all.setText("")
        self.action_collapse_all.setText("")
        self.action_resize_win.setText("")
        self.action_sync_maya_operator.setText("")
        self.action_sync_maya_operator_label.setText("")
        self.action_sync_maya_operator_label.setEnabled(False)

        self.__tab = QtTabCSWidget()
        self.__tab_import = QtTabItemCSWidget()
        self.__tab_file = QtTabItemCSWidget()
        self.__tab_edit = QtTabItemCSWidget()
        self.__tab_display = QtTabItemCSWidget()
        self.__tab_inspector = QtTabItemCSWidget()
        self.__tab_debug = QtTabItemCSWidget()

        self.__frame_edit_attribute = attribute.EditAttributeWidget()
        self.__frame_imports = imports.ImportsWidget()
        self.__frame_file = file.FileWidget()
        self.__frame_log = log.LogWidget()
        self.__frame_manage = manage.ManageWidget()
        self.__frame_node = node.NodeWidget()
        self.__frame_parse = parse.ParseWidget()
        self.__frame_scene = scene.SceneWidget()
        self.__frame_visualize = visualize.VisualizeWidget()

        self.__tab_import.scrollarea.layout.addWidget(self.__frame_imports)
        self.__tab_file.scrollarea.layout.addWidget(self.__frame_file)
        self.__tab_file.scrollarea.layout.addWidget(self.__frame_parse)
        self.__tab_edit.scrollarea.layout.addWidget(self.__frame_scene)
        self.__tab_edit.scrollarea.layout.addWidget(self.__frame_manage)
        self.__tab_edit.scrollarea.layout.addWidget(self.__frame_node)
        self.__tab_inspector.scrollarea.layout.addWidget(self.__frame_edit_attribute)
        self.__tab_display.scrollarea.layout.addWidget(self.__frame_visualize)
        self.__tab_debug.scrollarea.layout.addWidget(self.__frame_log)

        self.__tab.setStyleSheet(QtStyle.Tab)
        self.tab_bar = QtTabBarCSWidget()
        # self.tab_button = QtButtonCSWidget()
        # self.tab_button.setStyleSheet(QtButtonStyle.Transparent)
        # self.tab_bar.setTabButton(0, QtWidgets.QTabBar.LeftSide, self.tab_button)
        self.__tab.setTabBar(self.tab_bar)

        self.__tab.addTab(self.__tab_import, "Imports")

        self.__layout.addWidget(self.__tab)
        self.__menubar.addAction(self.action_reset)

        self.set_wheel_up_event(self.action_wheel_up)
        self.set_wheel_down_event(self.action_wheel_down)
        self.__menubar.addAction(self.action_expand_all)
        self.__menubar.addAction(self.action_collapse_all)
        self.__menubar.addAction(self.action_resize_win)
        self.__menubar.addAction(self.action_sync_maya_operator)
        self.__menubar.addAction(self.action_sync_maya_operator_label)
        self.setLayout(self.__layout)
        self.layout().setMenuBar(self.__menubar)

        Repository().ui.main = self

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

    def init_tabs_on_file_mode(self):
        self.__tab.removeTab(0)
        self.__tab.addTab(self.__tab_file, "File")

    def init_tabs_on_scene_mode(self):
        self.__tab.removeTab(0)
        self.__tab.addTab(self.__tab_edit, "Edit")
        self.__tab.addTab(self.__tab_display, "Display")
        self.__tab.addTab(self.__tab_inspector, "Inspector")
        self.__tab.addTab(self.__tab_debug, "Debug")
