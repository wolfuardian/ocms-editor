from ocmseditor.oe.utils.qt import QtFrameLayoutCSWidget, QtScrollareaCSWidget


class EditAttributeWidget(QtFrameLayoutCSWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.set_text("編輯屬性")

        self.scrollarea = QtScrollareaCSWidget()
