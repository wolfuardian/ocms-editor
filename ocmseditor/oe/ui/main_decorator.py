from ocmseditor.oe.ui.main import UIMain


def show_gui():
    from ocmseditor.oe.gui import show

    show()


class UIMainDecorator(UIMain):
    def __init__(self):
        super(UIMainDecorator, self).__init__()
        self.sync_maya_operator = False

        self.frames_toggle = True
        self.cur_frame_index = 0

        # self.tab.currentChanged.connect(self.tab_changed_event)

        self.action_reset.triggered.connect(show_gui)
        self.action_reset.setShortcut("Shift+`")

        self.action_wheel_up.triggered.connect(self.toggle_prev_frame)

        self.action_wheel_down.triggered.connect(self.toggle_next_frame)

        self.action_expand_all.triggered.connect(self.expand_frame_widgets)
        self.action_expand_all.setShortcut("Ctrl+Shift++")

        self.action_collapse_all.triggered.connect(self.collapse_frame_widgets)
        self.action_collapse_all.setShortcut("Ctrl+Shift+-")

        self.action_resize_win.triggered.connect(self.toggle_resize_win)
        self.action_resize_win.setShortcut("Shift+2")

        # self.action_sync_maya_operator.triggered.connect(self.toggle_sync_maya_operator)
        # self.action_sync_maya_operator.setShortcut("Shift+1")

        # self.frame_widgets[0].set_isolated_action(lambda: self.toggle_frame_by_index(0))
        # self.frame_widgets[1].set_isolated_action(lambda: self.toggle_frame_by_index(1))
        # self.frame_widgets[2].set_isolated_action(lambda: self.toggle_frame_by_index(2))
        # self.frame_widgets[3].set_isolated_action(lambda: self.toggle_frame_by_index(3))

        # self.toggle_frame_by_index(2)

    # def tab_changed_event(self, index):
    #     if index == 1:
    #         self.sync_maya_operator = True
    #         self.action_sync_maya_operator.setText("")
    #         self.action_sync_maya_operator.setIcon(
    #             qt.QtGui.QIcon(":/recordStandby.png")
    #         )
    #         self.action_sync_maya_operator_label.setText("同步中")
    #         handler.create_script_job()
    #     else:
    #         self.sync_maya_operator = False
    #         # self.action_sync_maya_operator.setText("同步中")
    #         self.action_sync_maya_operator.setIcon(qt.QtGui.QIcon(":/recording.png"))
    #         self.action_sync_maya_operator_label.setText("")
    #         handler.delete_script_job()

    def toggle_next_frame(self):
        self._increment_frame_index()
        self.toggle_frame_by_index(self.cur_frame_index)

    def toggle_prev_frame(self):
        self._decrement_frame_index()
        self.toggle_frame_by_index(self.cur_frame_index)

    def toggle_resize_win(self):
        self._update_window_size_factor()
        self._resize_window()

    # def toggle_sync_maya_operator(self):
    #     self.sync_maya_operator = not self.sync_maya_operator
    #     if self.sync_maya_operator:
    #         self.action_sync_maya_operator.setIcon(
    #             qt.QtGui.QIcon(":/recordStandby.png")
    #         )
    #         handler.create_script_job()
    #     else:
    #         self.action_sync_maya_operator.setIcon(qt.QtGui.QIcon(":/recording.png"))
    #         handler.delete_script_job()

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

    # def _resize_window(self):
    #     _fixed_width = qt.QtGui.QGuiApplication.primaryScreen().size().width() / 4
    #     self.setMinimumWidth(_fixed_width * (self.window_size_factor + 1))
    #     self.action_resize_win.setText("▮" if self.window_size_factor == 0 else "■")
