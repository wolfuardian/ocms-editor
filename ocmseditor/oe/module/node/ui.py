from ocmseditor.oe.utils.qt import QtFrameLayoutCSWidget, QtScrollareaCSWidget


class NodeWidget(QtFrameLayoutCSWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.set_text("節點")

        self.scrollarea = QtScrollareaCSWidget()
