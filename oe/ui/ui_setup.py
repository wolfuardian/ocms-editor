from maya.app.general import mayaMixin
from oe.utils import qt

import oe.tools as tools
from version import version as ver

class Setup(mayaMixin.MayaQWidgetDockableMixin, mayaMixin.MayaQWidgetBaseMixin, qt.QtDefaultCSWidget):
    def __init__(self, parent=tools.Maya.get_main_window()):
        super(Setup, self).__init__(parent)

        self.setWindowTitle(ver)
        self.setMinimumWidth(360)

        layout = qt.QtWidgets.QVBoxLayout()
        layout.setAlignment(qt.QtCore.Qt.AlignTop)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(0)

        # <editor-fold desc="CODE_BLOCK: Create Widget">
        bar = qt.QtWidgets.QMenuBar()

        tab = qt.QtTabCSWidget()
        tab_opt = qt.QtTabItemCSWidget()

        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Assembly Widget">

        tab.addTab(tab_opt, "")

        layout.addWidget(tab)

        self.setLayout(layout)

        self.layout().setMenuBar(bar)
        # </editor-fold>

        # <editor-fold desc="CODE_BLOCK: Public Variable">
        self.layout = layout

        self.bar = bar
        self.tab = tab
        self.tab_tool = tab_opt
        # </editor-fold>
