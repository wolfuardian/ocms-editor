import ocmseditor.core.tool as core

from ocmseditor import tool


class Widget(core.Widget):
    @classmethod
    def hide(cls, widget):
        widget.set_force_visible(False)

    @classmethod
    def show(cls, widget):
        widget.set_force_visible(True)

    @classmethod
    def enable(cls, widget):
        widget.setEnabled(True)

    @classmethod
    def disable(cls, widget):
        widget.setEnabled(False)

    @classmethod
    def set_text(cls, widget, text):
        widget.setText(text)
        widget.setCursorPosition(0)
