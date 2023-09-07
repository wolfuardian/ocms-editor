import oe.tools as tools

from oe import gui
from oe.ui import ui_setup

from oe.utils import qt


class Tweak(ui_setup.Setup):
    def __init__(self):
        super(Tweak, self).__init__()

        self.frames_toggle = True
        self.cur_frame_index = 0

        self.action_reset.triggered.connect(gui.show)
        self.action_reset.setShortcut("Shift+`")

        self.action_wheel_up.triggered.connect(self.toggle_prev_frame)

        self.action_wheel_down.triggered.connect(self.toggle_next_frame)

        self.action_expand_all.triggered.connect(self.expand_frame_widgets)
        self.action_expand_all.setShortcut("Ctrl+Shift++")

        self.action_collapse_all.triggered.connect(self.collapse_frame_widgets)
        self.action_collapse_all.setShortcut("Ctrl+Shift+-")

        self.action_resize_win.triggered.connect(self.toggle_resize_win)
        self.action_resize_win.setShortcut("Shift+2")

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
