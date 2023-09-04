import oe.tools as tools

from oe import gui
from oe.ui import ui_setup

from oe.utils import qt


class Tweak(ui_setup.Setup):
    def __init__(self):
        super(Tweak, self).__init__()

        self.frame_widget_toggle = True

        self.action_reset.triggered.connect(gui.show)
        self.action_reset.setShortcut("Shift+`")

        self.action_expand_all.triggered.connect(self.toggle_frame_widgets)
        self.action_expand_all.setShortcut("Shift+1")

        self.action_resize_win.triggered.connect(self.toggle_resize_win)
        self.action_resize_win.setShortcut("Shift+2")

    def toggle_frame_widgets(self):
        for frame_btn in self.frame_widgets:
            frame_btn.set_toggle(self.frame_widget_toggle)
        self.frame_widget_toggle = not self.frame_widget_toggle
        self.action_expand_all.setText("🙂" if self.frame_widget_toggle else "😮")

    def toggle_resize_win(self):
        self.window_size_factor += 1
        self.window_size_factor = self.window_size_factor % 2
        tools.Logging.gui_logger().info(
            "Current window size factor: {}".format(self.window_size_factor)
        )
        _fixed_width = qt.QtGui.QGuiApplication.primaryScreen().size().width() / 4
        self.setMinimumWidth(_fixed_width * (self.window_size_factor + 1))
        self.action_resize_win.setText("▮" if self.window_size_factor == 0 else "■")
