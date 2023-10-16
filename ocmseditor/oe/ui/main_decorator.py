from ocmseditor.oe.ui.main import UIMain
from ocmseditor.oe.utils.qt import QtGui
from ocmseditor.oe.handler import subscribe_events


def show_gui():
    from ocmseditor.oe.gui import show

    show()


class UIMainDecorator(UIMain):
    def __init__(self):
        super(UIMainDecorator, self).__init__()
        subscribe_events()

        self.__frames_toggle = True
        self.__cur_frame_index = 0

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

    def toggle_next_frame(self):
        self._increment_frame_index()
        self.toggle_frame_by_index(self.__cur_frame_index)

    def toggle_prev_frame(self):
        self._decrement_frame_index()
        self.toggle_frame_by_index(self.__cur_frame_index)

    def toggle_resize_win(self):
        self._update_window_size_factor()
        self._resize_window()

    def expand_frame_widgets(self):
        for frame_btn in self.__frame_widgets:
            frame_btn.set_toggle(True)
        self.__frames_toggle = False

    def collapse_frame_widgets(self):
        for frame_btn in self.__frame_widgets:
            frame_btn.set_toggle(False)
        self.__frames_toggle = True

    def isolate_frame_widgets(self, widget):
        for frame_btn in self.__frame_widgets:
            if frame_btn != widget:
                frame_btn.set_toggle(False)
        widget.set_toggle(True)
        self.__frames_toggle = False

    # Internal methods
    def toggle_frame_by_index(self, index):
        self.collapse_frame_widgets()
        self.__frame_widgets[index].set_toggle(True)

    def _increment_frame_index(self):
        self.__cur_frame_index = (self.__cur_frame_index + 1) % len(
            self.__frame_widgets
        )

    def _decrement_frame_index(self):
        self.__cur_frame_index = (self.__cur_frame_index - 1) % len(
            self.__frame_widgets
        )

    def _update_window_size_factor(self):
        self.window_size_factor += 1
        self.window_size_factor = self.window_size_factor % 2

    def _resize_window(self):
        self.__fixed_width = QtGui.QGuiApplication.primaryScreen().size().width() / 4
        self.setMinimumWidth(self.__fixed_width * (self.window_size_factor + 1))
