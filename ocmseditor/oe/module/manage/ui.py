from ocmseditor.oe.utils.qt import QtFrameLayoutCSWidget, QtScrollareaCSWidget


class ManageWidget(QtFrameLayoutCSWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.set_text("管理")

        self.scrollarea = QtScrollareaCSWidget()
