import sys
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore, QtGui


from ocmseditor.oe.constant import ICON_DIR, Fonts
from ocmseditor.oe.utils.qt_stylesheet import (
    QtStyle,
    QtLabelStyle,
    QtButtonStyle,
    QtGroupBoxStyle,
)


def get_main_window():
    maya_main_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(maya_main_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(maya_main_ptr), QtWidgets.QWidget)


class QtDefaultCSWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__wheel_up_action = None
        self.__wheel_down_action = None

        self.__visible_immediate = True

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.set_extra_stylesheet()

    def set_wheel_up_event(self, up_action):
        self.__wheel_up_action = up_action

    def set_wheel_down_event(self, down_action):
        self.__wheel_down_action = down_action

    def set_visible_immediate(self, visible):
        self.__visible_immediate = visible
        self.setVisible(visible)

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)

    def set_extra_stylesheet(self):
        self.setStyleSheet(self.styleSheet() + "\n" + QtStyle.Tooltip)


class QtTabCSWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)


class QtTabBarCSWidget(QtWidgets.QTabBar):
    def __init__(self):
        super().__init__()

    def set_icon(self, index, icon):
        if icon.startswith(":/"):
            self.setTabIcon(index, QtGui.QIcon(icon))
        else:
            __icon = (ICON_DIR / icon).resolve().__str__()
            try:
                self.setTabIcon(index, QtGui.QIcon(__icon))
            except Exception as e:
                print(e)


class QtTabItemCSWidget(QtDefaultCSWidget):
    def __init__(self):
        super().__init__()

        self.__layout = QtWidgets.QVBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(6)

        self.scrollarea = QtScrollareaCSWidget()

        self.__layout.addWidget(self.scrollarea)

        self.setLayout(self.__layout)

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

        self.__widget = QtDefaultCSWidget()

        self.__layout = QtWidgets.QVBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)

        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.setStyleSheet(QtStyle.Scrollarea)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.__layout.addLayout(self.layout)

        self.__widget.setLayout(self.__layout)

        self.setWidget(self.__widget)

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)


class QtFrameLayoutCSWidget(QtDefaultCSWidget):
    def __init__(self, text=""):
        super().__init__()

        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        self.__layout = QtWidgets.QVBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)
        self.__layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.__layout)

        self.__frame_btn = QtFrameButtonCSWidget()
        self.__frame_btn.setText(text)
        self.__frame_btn.setObjectName("frame_btn")
        self.__frame_btn.setFont(QtGui.QFont(Fonts.SegoeUI, 10, QtGui.QFont.ExtraBold))
        self.__frame_btn.collapsed.add(self.__on_collapsed)
        self.__frame_btn.expanded.add(self.__on_expanded)
        self.__frame_btn.isolated.add(self.__on_isolated)

        self.__frame = QtWidgets.QWidget(self)
        self.__frame.setObjectName("frame_widget")
        self.__frame.setContentsMargins(3, 3, 3, 3)
        self.__frame.setStyleSheet(QtStyle.Frame)

        self.__frame_layout = QtWidgets.QVBoxLayout(self.__frame)
        self.__frame_layout.setObjectName("frame_layout")
        self.__frame_layout.setContentsMargins(0, 0, 0, 0)
        self.__frame_layout.setSpacing(0)

        self.layout().addWidget(self.__frame_btn)
        self.layout().addWidget(self.__frame)

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)

    @property
    def frame_btn(self):
        return self.__frame_btn

    @property
    def frame_layout(self):
        return self.__frame_layout

    def collapsed(self):
        self.__on_collapsed()

    def __on_collapsed(self):
        for item in self.__frame.findChildren(QtWidgets.QWidget):
            item.setVisible(getattr(item, "__visible_immediate", False))

    def __on_expanded(self):
        for item in self.__frame.findChildren(QtWidgets.QWidget):
            item.setVisible(getattr(item, "__visible_immediate", True))

    def __on_isolated(self):
        self.set_toggle(True)

    def set_text(self, text):
        self.__frame_btn.setText(text)

    def set_toggle(self, toggle):
        self.__frame_btn.toggle = toggle

    def set_isolated_action(self, action):
        self.__frame_btn.isolated.add(action)


class QtFramelessLayoutCSWidget(QtDefaultCSWidget):
    def __init__(self):
        super().__init__()

        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        self.__layout = QtWidgets.QVBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)
        self.__layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.__layout)

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)


class QtFrameButtonCSWidget(QtDefaultCSWidget):
    def __init__(self, label=""):
        super().__init__()

        self.__close_pix = QtGui.QPixmap(":/teRightArrow.png")
        self.__open_pix = QtGui.QPixmap(":/teDownArrow.png")

        self.setMinimumSize(288, 24)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.setAutoFillBackground(True)

        self.__color_default = (39, 39, 39)
        self.__color_hover = (46, 46, 46)

        self.setBackgroundColor(self.__color_default)  # Dark

        self.__layout = QtWidgets.QHBoxLayout()
        self.__layout.setContentsMargins(5, 0, 5, 0)
        self.__layout.setSpacing(12)
        self.__layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.__icon = QtWidgets.QLabel()
        self.__icon.setPixmap(self.__close_pix)
        self.__layout.addWidget(self.__icon)

        self.__label = QtWidgets.QLabel(" " + label)
        self.__layout.addWidget(self.__label)

        self.__isolate_btn = QtButtonCSWidget()
        self.__isolate_btn.set_icon(":/scale_M.png")
        self.__isolate_btn.setFixedWidth(20)
        self.__isolate_btn.setFixedHeight(20)
        self.__isolate_btn.setStyleSheet(QtButtonStyle.Transparent)
        self.__isolate_btn.clicked.connect(lambda: self.__isolated.emit())
        self.__layout.addStretch()
        self.__layout.addWidget(self.__isolate_btn)

        self.setLayout(self.__layout)

        class _Listener(object):
            def __init__(self, container):
                self.__container = container

            def add(self, func):
                self.__container.append(func)

            def remove(self, func):
                if func in self.__container:
                    self.__container.remove(func)

        class Subject(object):
            def __init__(self):
                self.__functions = []
                self.__listener = _Listener(self.__functions)

            def emit(self, *args, **kwargs):
                for func in self.__functions:
                    func(*args, **kwargs)

            @property
            def listen(self):
                # type: () -> _Listener
                return self.__listener

        self.__toggle = True
        self.__collapsed = Subject()
        self.__expanded = Subject()
        self.__isolated = Subject()
        self.__collapsed.listen.add(lambda: self.__icon.setPixmap(self.__close_pix))
        self.__expanded.listen.add(lambda: self.__icon.setPixmap(self.__open_pix))

    @property
    def toggle(self):
        return self.__toggle

    @toggle.setter
    def toggle(self, value):
        self.__toggle = value
        self.__expanded.emit() if self.__toggle else self.__collapsed.emit()

    @property
    def collapsed(self):
        return self.__collapsed.listen

    @property
    def expanded(self):
        return self.__expanded.listen

    @property
    def isolated(self):
        return self.__isolated.listen

    def setFont(self, font):
        self.__label.setFont(font)

    def setText(self, text):
        self.__label.setText(text)

    def setBackgroundColor(self, color):
        __palette = self.palette()
        __palette.setColor(
            self.backgroundRole(), QtGui.QColor(color[0], color[1], color[2])
        )
        self.setPalette(__palette)

    def mouseReleaseEvent(self, *args, **kwargs):
        self.__toggle = not self.__toggle
        self.__expanded.emit() if self.__toggle else self.__collapsed.emit()

    def enterEvent(self, *args, **kwargs):
        self.setBackgroundColor(self.__color_hover)

    def leaveEvent(self, *args, **kwargs):
        self.setBackgroundColor(self.__color_default)


class QtGroupBoxCSWidget(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__()
        self.__visible_immediate = True
        self.__font = QtGui.QFont(Fonts.MicrosoftJhengHei, 8, QtGui.QFont.Bold)
        self.__font.setLetterSpacing(QtGui.QFont.PercentageSpacing, 110)
        self.setFont(QtGui.QFont(self.__font))

    def set_visible_immediate(self, visible):
        self.__visible_immediate = visible
        self.setVisible(visible)

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)


class QtGroupHBoxCSWidget(QtGroupBoxCSWidget):
    def __init__(self):
        super().__init__()
        self.__visible_immediate = True
        self.__layout = QtWidgets.QHBoxLayout()
        self.__layout.setAlignment(QtCore.Qt.AlignTop)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)
        self.setLayout(self.__layout)
        self.layout = self.__layout
        self.layout_content: list[QtWidgets] = []
        self.setStyleSheet(QtGroupBoxStyle.Default)

    def set_visible_immediate(self, visible):
        self.__visible_immediate = visible
        self.setVisible(visible)

    def set_stylesheet_additional(self, style):
        self.setStyleSheet(self.styleSheet() + "\n" + style)

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)


class QtGroupVBoxCSWidget(QtGroupBoxCSWidget):
    def __init__(self):
        super().__init__()
        self.__visible_immediate = True
        self.__layout = QtWidgets.QVBoxLayout()
        self.__layout.setAlignment(QtCore.Qt.AlignTop)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)
        self.setLayout(self.__layout)
        self.layout = self.__layout
        self.layout_content: list[QtWidgets] = []
        self.setStyleSheet(QtGroupBoxStyle.Default)

    def set_visible_immediate(self, visible):
        self.__visible_immediate = visible
        self.setVisible(visible)

    def set_stylesheet_additional(self, style):
        self.setStyleSheet(self.styleSheet() + "\n" + style)

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)


class QtButtonCSWidget(QtWidgets.QPushButton):
    def __init__(self):
        super().__init__()
        self.__visible_immediate = True
        self.setFont(QtGui.QFont(Fonts.SegoeUI, 8, QtGui.QFont.Normal))
        self.setStyleSheet(QtButtonStyle.Default)

    def set_icon(self, icon):
        if icon.startswith(":/"):
            self.setIcon(QtGui.QIcon(icon))
        else:
            __icon = (ICON_DIR / icon).resolve().__str__()
            try:
                self.setTabIcon(QtGui.QIcon(__icon))
            except Exception as e:
                print(e)

    def set_visible_immediate(self, visible):
        self.__visible_immediate = visible
        self.setVisible(visible)

    def set_stylesheet_additional(self, style):
        self.setStyleSheet(self.styleSheet() + "\n" + style)

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)


class QtBigButtonCSWidget(QtButtonCSWidget):
    def __init__(self):
        super().__init__()
        self.__layout = QtWidgets.QVBoxLayout()
        self.__icon = QtWidgets.QLabel(self)
        self.__icon.setAlignment(QtCore.Qt.AlignCenter)

        self.__label = QtWidgets.QLabel()
        self.__label.setAlignment(QtCore.Qt.AlignCenter)
        self.__layout.addWidget(self.__icon)
        self.__layout.addWidget(self.__label)
        self.setLayout(self.__layout)

    def set_icon(self, icon):
        __size = (32, 32)
        if icon.startswith(":/"):
            pixmap = QtGui.QPixmap(icon)
            scaled_pixmap = pixmap.scaled(
                *__size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
            )
            self.__icon.setPixmap(scaled_pixmap)
        else:
            __icon = (ICON_DIR / icon).resolve().__str__()
            try:
                pixmap = QtGui.QPixmap(__icon)
                scaled_pixmap = pixmap.scaled(
                    *__size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
                )
                self.__icon.setPixmap(scaled_pixmap)
            except Exception as e:
                print(e)

    def setText(self, text):
        self.__label.setText(text)


class QtHeadingLabelCSWidget(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.__visible_immediate = True
        # self.setFont(QtGui.QFont(Fonts.SegoeUI, 8, QtGui.QFont.Normal))
        self.setStyleSheet(QtButtonStyle.Default)

    def set_heading(self, level):
        if level == 0:
            self.setStyleSheet(QtLabelStyle.Heading_0)
        elif level == 1:
            self.setStyleSheet(QtLabelStyle.Heading_1)
        elif level == 2:
            self.setStyleSheet(QtLabelStyle.Heading_2)
        elif level == 3:
            self.setStyleSheet(QtLabelStyle.Heading_3)
        elif level == 4:
            self.setStyleSheet(QtLabelStyle.Heading_4)
        elif level == 5:
            self.setStyleSheet(QtLabelStyle.Heading_5)
        else:
            print("Error: Heading level out of range.")
            return

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)
