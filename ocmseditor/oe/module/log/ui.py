from ocmseditor.oe.utils.qt import QtFrameLayoutCSWidget, QtScrollareaCSWidget


class LogWidget(QtFrameLayoutCSWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.set_text("紀錄")

        self.scrollarea = QtScrollareaCSWidget()
