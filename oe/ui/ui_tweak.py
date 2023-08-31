from oe.utils import qt

from oe.ui import ui_setup
from oe import gui


class Tweak(ui_setup.Setup):
    def __init__(self):
        super(Tweak, self).__init__()

        self.frame_widget_toggle = False

        self.action_reset.triggered.connect(gui.show)
        self.action_reset.setShortcut("Alt+`")

        self.action_expand_all.triggered.connect(self.toggle_frame_widgets)
        self.action_expand_all.setShortcut("Shift+1")

    def toggle_frame_widgets(self):
        for frame_btn in self.frame_widgets:
            frame_btn.set_toggle(self.frame_widget_toggle)
        self.frame_widget_toggle = not self.frame_widget_toggle
        self.action_expand_all.setText("🙂" if self.frame_widget_toggle else "😮")