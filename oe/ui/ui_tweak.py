from oe.ui import ui_setup
from oe import gui


class Tweak(ui_setup.Setup):
    def __init__(self):
        super(Tweak, self).__init__()

        self.action_reset.triggered.connect(gui.show)
        self.action_reset.setShortcut("Alt+`")
