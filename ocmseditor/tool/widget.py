import ocmseditor.core.tool as core


class Widget(core.Widget):
    @classmethod
    def disable(cls, widget):
        """
        禁用指定的部件。

        參數:
            widget: 要禁用的 GUI 部件對象。
        """
        widget.setEnabled(False)

    @classmethod
    def enable(cls, widget):
        """
        啟用指定的部件。

        參數:
            widget: 要啟用的 GUI 部件對象。
        """
        widget.setEnabled(True)

    @classmethod
    def show_hide(cls, widget, show):
        """
        根據指定的布爾值顯示或隱藏部件。

        參數:
            widget: 要顯示或隱藏的 GUI 部件對象。
            show: 布爾值，True 表示顯示，False 表示隱藏。
        """
        widget.set_force_visible(show)

    @classmethod
    def set_text(cls, widget, text):
        """
        為指定的部件設置文本並將光標位置重置為0。

        參數:
            widget: 要設置文本的 GUI 部件對象。
            text: 要設置的文本字符串。
        """
        widget.setText(text)
        widget.setCursorPosition(0)
