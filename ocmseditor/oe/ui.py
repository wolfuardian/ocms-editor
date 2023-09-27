from pathlib import Path
from maya.app.general import mayaMixin

import ocmseditor.oe.helper as helper
import ocmseditor.oe.handler as handler

from ocmseditor.oe import qt

from ocmseditor import win
from ocmseditor import tool
from ocmseditor.oe import module as module


def version():
    path = Path(__file__).resolve().parent.parent.parent / "version.txt"
    with open(path, "r") as f:
        return f.read().strip()


class MainUI(
    mayaMixin.MayaQWidgetDockableMixin,
    mayaMixin.MayaQWidgetBaseMixin,
    qt.QtDefaultCSWidget,
):
    def __init__(self, parent=tool.Maya.get_main_window()):
        super(MainUI, self).__init__(parent)

        self.setWindowTitle(version())
        self.window_size_factor = 1.0

        layout = qt.QtWidgets.QVBoxLayout()
        layout.setAlignment(qt.QtCore.Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        menubar = qt.QtWidgets.QMenuBar()

        action_wheel_up = qt.QtWidgets.QAction()
        action_wheel_down = qt.QtWidgets.QAction()
        action_reset = qt.QtWidgets.QAction()
        action_expand_all = qt.QtWidgets.QAction()
        action_collapse_all = qt.QtWidgets.QAction()
        action_resize_win = qt.QtWidgets.QAction()
        action_sync_maya_operator = qt.QtWidgets.QAction()
        action_sync_maya_operator_label = qt.QtWidgets.QAction()

        action_reset.setIcon(qt.QtGui.QIcon(":/reloadReference.png"))
        action_expand_all.setIcon(qt.QtGui.QIcon(":/expandInfluenceList.png"))
        action_collapse_all.setIcon(qt.QtGui.QIcon(":/retractInfluenceList.png"))
        action_resize_win.setIcon(qt.QtGui.QIcon(":/nodeGrapherToggleView.png"))
        action_sync_maya_operator.setIcon(qt.QtGui.QIcon(":/recording.png"))
        action_sync_maya_operator_label.setText("")
        action_sync_maya_operator_label.setEnabled(False)

        tab = qt.QtTabCSWidget()
        tab_load = qt.QtTabItemCSWidget()
        tab_res = qt.QtTabItemCSWidget()
        tab_edit = qt.QtTabItemCSWidget()
        tab_save = qt.QtTabItemCSWidget()

        frame_set_project = module.SetProjectDirectoryCSWidget()
        frame_parse_xml = module.ParseXMLCSWidget()
        frame_parse_res = module.ParseResourceCSWidget()
        frame_write_xml = module.WriteXMLCSWidget()
        frame_tool_box = module.ToolBoxCSWidget()
        frame_edit_attr = module.EditAttributeCSWidget()

        tab_load.layout.addWidget(frame_set_project)
        tab_load.layout.addWidget(frame_parse_xml)
        tab_res.layout.addWidget(frame_parse_res)
        tab_edit.layout.addWidget(frame_edit_attr)
        tab_save.layout.addWidget(frame_write_xml)

        tab.addTab(tab_load, "   專案 / 初始化   ")
        tab.addTab(tab_edit, "   編輯   ")
        tab.addTab(tab_res, "   資源工具   ")
        tab.addTab(tab_save, "   輸出   ")
        layout.addWidget(tab)
        layout.addWidget(frame_tool_box)
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
        self.tab_tool = tab_load

        self.action_reset = action_reset
        self.action_wheel_up = action_wheel_up
        self.action_wheel_down = action_wheel_down
        self.action_expand_all = action_expand_all
        self.action_collapse_all = action_collapse_all
        self.action_resize_win = action_resize_win
        self.action_sync_maya_operator = action_sync_maya_operator
        self.action_sync_maya_operator_label = action_sync_maya_operator_label

        self.frame_widgets = [
            frame_set_project,
            frame_parse_xml,
            frame_parse_res,
            frame_write_xml,
        ]

        ocms = tool.OCMS.get_ocms()
        ocms.ui.context.setdefault("global", self)
        ocms.ui.context.setdefault("frame_set_project", frame_set_project)
        ocms.ui.context.setdefault("frame_parse_xml", frame_parse_xml)
        ocms.ui.context.setdefault("frame_parse_res", frame_parse_res)
        ocms.ui.context.setdefault("frame_write_xml", frame_write_xml)
        ocms.ui.context.setdefault("frame_tool_box", frame_tool_box)
        ocms.ui.context.setdefault("frame_edit_attr", frame_edit_attr)

        self.toggle_resize_win()


class Tweak(MainUI):
    def __init__(self):
        super(Tweak, self).__init__()
        self.sync_maya_operator = False

        self.frames_toggle = True
        self.cur_frame_index = 0

        self.tab.currentChanged.connect(self.tab_changed_event)

        self.action_reset.triggered.connect(win.show)
        self.action_reset.setShortcut("Shift+`")

        self.action_wheel_up.triggered.connect(self.toggle_prev_frame)

        self.action_wheel_down.triggered.connect(self.toggle_next_frame)

        self.action_expand_all.triggered.connect(self.expand_frame_widgets)
        self.action_expand_all.setShortcut("Ctrl+Shift++")

        self.action_collapse_all.triggered.connect(self.collapse_frame_widgets)
        self.action_collapse_all.setShortcut("Ctrl+Shift+-")

        self.action_resize_win.triggered.connect(self.toggle_resize_win)
        self.action_resize_win.setShortcut("Shift+2")

        self.action_sync_maya_operator.triggered.connect(self.toggle_sync_maya_operator)
        self.action_sync_maya_operator.setShortcut("Shift+1")

        self.frame_widgets[0].set_isolated_action(lambda: self.toggle_frame_by_index(0))
        self.frame_widgets[1].set_isolated_action(lambda: self.toggle_frame_by_index(1))
        self.frame_widgets[2].set_isolated_action(lambda: self.toggle_frame_by_index(2))
        self.frame_widgets[3].set_isolated_action(lambda: self.toggle_frame_by_index(3))

        # self.toggle_frame_by_index(2)

    def tab_changed_event(self, index):
        if index == 1:
            self.sync_maya_operator = True
            self.action_sync_maya_operator.setText("")
            self.action_sync_maya_operator.setIcon(
                qt.QtGui.QIcon(":/recordStandby.png")
            )
            self.action_sync_maya_operator_label.setText("同步中")
            handler.create_script_job()
        else:
            self.sync_maya_operator = False
            # self.action_sync_maya_operator.setText("同步中")
            self.action_sync_maya_operator.setIcon(qt.QtGui.QIcon(":/recording.png"))
            self.action_sync_maya_operator_label.setText("")
            handler.delete_script_job()

    def toggle_next_frame(self):
        self._increment_frame_index()
        self.toggle_frame_by_index(self.cur_frame_index)

    def toggle_prev_frame(self):
        self._decrement_frame_index()
        self.toggle_frame_by_index(self.cur_frame_index)

    def toggle_resize_win(self):
        self._update_window_size_factor()
        self._resize_window()

    def toggle_sync_maya_operator(self):
        self.sync_maya_operator = not self.sync_maya_operator
        if self.sync_maya_operator:
            self.action_sync_maya_operator.setIcon(
                qt.QtGui.QIcon(":/recordStandby.png")
            )
            handler.create_script_job()
        else:
            self.action_sync_maya_operator.setIcon(qt.QtGui.QIcon(":/recording.png"))
            handler.delete_script_job()

    def expand_frame_widgets(self):
        for frame_btn in self.frame_widgets:
            frame_btn.set_toggle(True)
        self.frames_toggle = False

    def collapse_frame_widgets(self):
        for frame_btn in self.frame_widgets:
            frame_btn.set_toggle(False)
        self.frames_toggle = True

    def isolate_frame_widgets(self, widget):
        for frame_btn in self.frame_widgets:
            if frame_btn != widget:
                frame_btn.set_toggle(False)
        widget.set_toggle(True)
        self.frames_toggle = False

    # Internal methods
    def toggle_frame_by_index(self, index):
        self.collapse_frame_widgets()
        self.frame_widgets[index].set_toggle(True)

    def _increment_frame_index(self):
        self.cur_frame_index = (self.cur_frame_index + 1) % len(self.frame_widgets)

    def _decrement_frame_index(self):
        self.cur_frame_index = (self.cur_frame_index - 1) % len(self.frame_widgets)

    def _update_window_size_factor(self):
        self.window_size_factor += 1
        self.window_size_factor = self.window_size_factor % 2

    def _resize_window(self):
        _fixed_width = qt.QtGui.QGuiApplication.primaryScreen().size().width() / 4
        self.setMinimumWidth(_fixed_width * (self.window_size_factor + 1))
        self.action_resize_win.setText("▮" if self.window_size_factor == 0 else "■")


def update_top_level_ui():
    helper.Logger.info(
        __name__, "Updating TOP-LEVEL UI ---------------------------------- //"
    )

    # from ocmseditor.oe.module.editattr import operator as editattr_op

    ocms = tool.OCMS.get_ocms()

    from ocmseditor.oe.module.setproject import operator as __op
    __ui = ocms.ui.context.get("frame_set_project")
    __op.op_fetch_project_path(__ui)

    from ocmseditor.oe.module.parsexml import operator as __op
    __ui = ocms.ui.context.get("frame_parse_xml")
    __op.op_fetch_xml_filepath(__ui)

    from ocmseditor.oe.module.parseres import operator as __op
    __ui = ocms.ui.context.get("frame_parse_res")
    __op.op_fetch_resource_path(__ui)

    from ocmseditor.oe.module.toolbox import operator as __op
    __ui = ocms.ui.context.get("frame_tool_box")
    __op.op_fetch_data(__ui)

    # from ocmseditor.oe.module.writexml import operator as __op
    __ui = ocms.ui.context.get("frame_write_xml")
    # __op.op_fetch_xml_export_filepath(__ui)

    # from ocmseditor.oe.module.editattr import operator as __op
    __ui = ocms.ui.context.get("frame_edit_attr")
    # __op.op_fetch_xml_export_filepath(__ui)

    helper.Logger.info(
        __name__, "Finished updating TOP-LEVEL UI ------------------------- //"
    )


def toggle_frame_expand_by_index(index):
    ocms = tool.OCMS.get_ocms()
    global_ui = ocms.ui.context.get("global")
    global_ui.toggle_frame_by_index(index)


def toggle_frame_expand_by_widget(widget):
    ocms = tool.OCMS.get_ocms()
    global_ui = ocms.ui.context.get("global")
    global_ui.isolate_frame_widgets(widget)
