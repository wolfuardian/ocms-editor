import sys
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore, QtGui


from ocmseditor.oe.constant import Fonts
from ocmseditor.oe.utils.qt_stylesheet import QtStylesheet


def get_main_window():
    maya_main_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(maya_main_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(maya_main_ptr), QtWidgets.QWidget)

# class CS_QBoxLayout(QtWidgets.QGroupBox):
#     def __init__(self):
#         super().__init__()
#
#
# class CS_QVBoxLayout(QtWidgets.QVBoxLayout):
#     def __init__(self):
#         super().__init__()

class QtDefaultCSWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.cooling_down = False
        self.cool_down_timer = QtCore.QTimer(self)
        self.cool_down_timer.setSingleShot(True)
        self.cool_down_timer.timeout.connect(self.reset_cool_down)

        self.wheel_up_action = None
        self.wheel_down_action = None

        self.force_visible = True

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.set_extra_stylesheet()

    def reset_cool_down(self):
        self.cooling_down = False

    def set_wheel_up_event(self, up_action):
        self.wheel_up_action = up_action

    def set_wheel_down_event(self, down_action):
        self.wheel_down_action = down_action

    def set_force_visible(self, visible):
        self.force_visible = visible
        self.setVisible(visible)

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)

    def set_extra_stylesheet(self):
        stylesheet = self.styleSheet() + "\n" + QtStylesheet.Tooltip
        self.setStyleSheet(stylesheet)

    def wheelEvent(self, event):
        if self.cooling_down:
            return

        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            angle = event.angleDelta().y()
            if angle > 0 and self.wheel_up_action:
                self.wheel_up_action.trigger()
            elif angle < 0 and self.wheel_down_action:
                self.wheel_down_action.trigger()

            self.cooling_down = True
            self.cool_down_timer.start(50)

        else:
            super().wheelEvent(event)


class QtTabCSWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)


class QtTabItemCSWidget(QtDefaultCSWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        scrollarea = QtScrollareaCSWidget()
        scrollarea.layout.setSpacing(3)

        layout.addWidget(scrollarea)

        self.setLayout(layout)

        # --------------------------------------------
        self.layout = scrollarea.layout
        # --------------------------------------------

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)


class QtScrollareaCSWidget(QtWidgets.QScrollArea):
    def __init__(self):
        super().__init__()

        self.setWidgetResizable(True)

        widget = QtDefaultCSWidget()

        layout = QtWidgets.QVBoxLayout()
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.setStyleSheet(
            f"""
            QScrollArea {{
                border: None;
            }}
            """
        )
        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setAlignment(QtCore.Qt.AlignTop)

        layout.addLayout(content_layout)

        widget.setLayout(layout)

        self.setWidget(widget)

        # --------------------------------------------
        self.layout = content_layout
        # --------------------------------------------

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)


