from maya.app.general import mayaMixin

from ocmseditor.oe import qt

from ocmseditor import win
from ocmseditor import tool
from ocmseditor.oe import ocms
from ocmseditor.oe import module as module
from pathlib import Path


def version():
    path = Path(__file__).resolve().parent.parent.parent / "version.txt"
    with open(path, "r") as f:
        return f.read().strip()


class Setup(
    mayaMixin.MayaQWidgetDockableMixin,
    mayaMixin.MayaQWidgetBaseMixin,
    qt.QtDefaultCSWidget,
):
    def __init__(self, parent=tool.Maya.get_main_window()):
        super(Setup, self).__init__(parent)

        self.setWindowTitle(version())
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
        frame_exportxml = module.ExportXMLCSWidget()

        tab_load.layout.addWidget(frame_set_project)
        tab_load.layout.addWidget(frame_parse_xml)
        tab_load.layout.addWidget(frame_parse_res)
        tab_load.layout.addWidget(frame_import_res)
        tab_save.layout.addWidget(frame_exportxml)

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
            frame_exportxml,
        ]

        ocms.UIStore.ui.setdefault("frame_set_project", frame_set_project)
        ocms.UIStore.ui.setdefault("frame_parse_xml", frame_parse_xml)
        ocms.UIStore.ui.setdefault("frame_parse_res", frame_parse_res)
        ocms.UIStore.ui.setdefault("frame_import_res", frame_import_res)
        ocms.UIStore.ui.setdefault("frame_exportxml", frame_exportxml)

        self.toggle_resize_win()


class Tweak(Setup):
    def __init__(self):
        super(Tweak, self).__init__()

        self.frames_toggle = True
        self.cur_frame_index = 0

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

        self.frame_widgets[0].set_isolated_action(
            lambda: self._toggle_frame_by_index(0)
        )
        self.frame_widgets[1].set_isolated_action(
            lambda: self._toggle_frame_by_index(1)
        )
        self.frame_widgets[2].set_isolated_action(
            lambda: self._toggle_frame_by_index(2)
        )
        self.frame_widgets[3].set_isolated_action(
            lambda: self._toggle_frame_by_index(3)
        )
        self.frame_widgets[4].set_isolated_action(
            lambda: self._toggle_frame_by_index(4)
        )

    def toggle_next_frame(self):
        self._increment_frame_index()
        self._toggle_frame_by_index(self.cur_frame_index)

    def toggle_prev_frame(self):
        self._decrement_frame_index()
        self._toggle_frame_by_index(self.cur_frame_index)

    def toggle_resize_win(self):
        self._update_window_size_factor()
        self._resize_window()

    def expand_frame_widgets(self):
        for frame_btn in self.frame_widgets:
            frame_btn.set_toggle(True)
        self.frames_toggle = False

    def collapse_frame_widgets(self):
        for frame_btn in self.frame_widgets:
            frame_btn.set_toggle(False)
        self.frames_toggle = True

    def isolate_frame_widgets(self, frame):
        for frame_btn in self.frame_widgets:
            if frame_btn != frame:
                frame_btn.set_toggle(False)
        frame.set_toggle(True)
        self.frames_toggle = False

    # Internal methods
    def _toggle_frame_by_index(self, index):
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
