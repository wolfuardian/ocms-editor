from ocmseditor.oe.utils.qt import QtFrameLayoutCSWidget, QtScrollareaCSWidget


class ParseWidget(QtFrameLayoutCSWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.set_text("分析")

        self.scrollarea = QtScrollareaCSWidget()
