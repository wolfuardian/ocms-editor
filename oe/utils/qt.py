from PySide2 import QtWidgets, QtCore, QtGui

from oe.refer import Qt as qt_
from oe.refer import Registry as reg_

from oe.tools.registry import Registry


class QtFonts:
    Fixedsys = "Fixedsys"
    SegoeUI = "Segoe UI"
    SimSun = "SimSun"
    SimHei = "SimHei"
    MicrosoftYaHei = "Microsoft YaHei"
    MicrosoftJhengHei = "Microsoft JhengHei"
    NSimSun = "NSimSun"
    PMingLiU = "PMingLiU"
    MingLiU = "MingLiU"
    DFKaiSB = "DFKai-SB"
    FangSong = "FangSong"
    KaiTi = "KaiTi"
    FangSong_GB2312 = "FangSong_GB2312"
    KaiTi_GB2312 = "KaiTi_GB2312"
    MSShellDlg2 = "MS Shell Dlg 2"
    HeitiTC = "Heiti TC"


# Default Widget
class QtDefaultCSWidget(QtWidgets.QWidget):
    """Custom QWidget subclass"""

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.is_cooling_down = False
        self.cool_down_timer = QtCore.QTimer(self)
        self.cool_down_timer.setSingleShot(True)
        self.cool_down_timer.timeout.connect(self.reset_cool_down)

        self.wheel_up_action = None
        self.wheel_down_action = None

        self.force_visible = True

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.set_extra_stylesheet()

    def reset_cool_down(self):
        self.is_cooling_down = False

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
        if self.is_cooling_down:
            return

        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            angle = event.angleDelta().y()
            if angle > 0 and self.wheel_up_action:
                self.wheel_up_action.trigger()
            elif angle < 0 and self.wheel_down_action:
                self.wheel_down_action.trigger()

            self.is_cooling_down = True
            self.cool_down_timer.start(50)

        else:
            super().wheelEvent(event)


# Basic Widget
class QtCheckBoxCSWidget(QtWidgets.QCheckBox):
    """Custom QCheckBox subclass"""

    def __init__(self, status=None):
        super().__init__()

        if status:
            self.set_status(status)
        else:
            self.set_status(QtCheckBoxStatus.Default)

        self.set_extra_stylesheet()

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)

    def set_status(self, status):
        self.setStyleSheet(status)

    def set_extra_stylesheet(self):
        stylesheet = self.styleSheet() + "\n" + QtStylesheet.Tooltip
        self.setStyleSheet(stylesheet)


class QtLabelCSWidget(QtWidgets.QLabel):
    """Custom QLabel subclass"""

    def __init__(self, parent=None, text=None, status=None):
        super().__init__(parent)

        if text:
            self.setText(text)
        if status:
            self.set_status(status)
        else:
            self.set_status(QtLabelStatus.Default)

        self.set_extra_stylesheet()

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)

    def set_status(self, status):
        self.setStyleSheet(status)

    def set_extra_stylesheet(self):
        stylesheet = self.styleSheet() + "\n" + QtStylesheet.Tooltip
        self.setStyleSheet(stylesheet)


class QtLineEditCSWidget(QtWidgets.QLineEdit):
    """Custom QLineEdit subclass"""

    def __init__(self, status=None):
        super().__init__()

        if status:
            self.set_status(status)
        else:
            self.set_status(QtLineEditStatus.Default)

        self.set_extra_stylesheet()

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)

    def set_status(self, status):
        self.setStyleSheet(status)

    def set_extra_stylesheet(self):
        stylesheet = self.styleSheet() + "\n" + QtStylesheet.Tooltip
        self.setStyleSheet(stylesheet)


class QtButtonCSWidget(QtWidgets.QPushButton):
    """Custom QPushButton subclass"""

    def __init__(
        self,
        parent=None,
        text=None,
        icon=None,
        spacing=None,
        width=None,
        height=None,
        status=None,
    ):
        super().__init__(parent)
        self.force_visible = True

        font = QtGui.QFont(QtFonts.SegoeUI, 8, QtGui.QFont.Normal)
        self.setFont(font)

        if icon:
            project_dir = Registry.get_value(
                reg_.REG_KEY, reg_.REG_SUB, "Pref_ModuleProjectDirectory", ""
            )
            icon_filepath = project_dir + qt_.ICON_DIR + icon
            try:
                self.setIcon(QtGui.QIcon(icon_filepath))
            except Exception as e:
                print(e)
        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)
        if spacing:
            text = " " * spacing + text + " " * spacing
        if text:
            self.setText(text)
        if status:
            self.set_status(status)
        else:
            self.set_status(QtButtonStatus.Default)

        self.set_extra_stylesheet()

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)

    def set_icon(self, icon):
        project_dir = Registry.get_value(
            reg_.REG_KEY, reg_.REG_SUB, "Pref_ModuleProjectDirectory", ""
        )
        icon_filepath = project_dir + qt_.ICON_DIR + icon
        try:
            self.setIcon(QtGui.QIcon(icon_filepath))
        except Exception as e:
            print(e)

    def set_text(self, text):
        self.setText(text)

    def set_width(self, width):
        self.setFixedWidth(width)

    def set_height(self, height):
        self.setFixedHeight(height)

    def set_spacing(self, spacing):
        text = " " * spacing + self.text() + " " * spacing
        self.setText(text)

    def set_force_visible(self, visible):
        self.force_visible = visible
        self.setVisible(visible)

    def set_status(self, status):
        self.setStyleSheet(status)

    def set_extra_stylesheet(self):
        stylesheet = self.styleSheet() + "\n" + QtStylesheet.Tooltip
        self.setStyleSheet(stylesheet)


class QtTabCSWidget(QtWidgets.QTabWidget):
    """Custom QTabWidget subclass"""

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)


class QtTabItemCSWidget(QtDefaultCSWidget):
    """Custom QTabItemWidget subclass"""

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        scrollarea = QtScrollareaCSWidget(margin=(3, 3, 3, 3))
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
    """Custom QScrollArea subclass"""

    def __init__(self, parent=None, margin=(0, 0, 0, 0), spacing=6):
        super().__init__(parent)
        self.setWidgetResizable(True)

        widget = QtDefaultCSWidget()

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(*margin)
        layout.setSpacing(spacing)
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


class QtFrameLayoutCSWidget(QtDefaultCSWidget):
    """Custom QtFrameLayout subclass, works in conjunction with QtFrameButtonWidget to form a single widget"""

    def __init__(self, parent=None, text="", width=0, height=60):
        super().__init__(parent)

        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(layout)

        self.__frame_btn = QtFrameButtonCSWidget("Frame Button")
        self.__frame_btn.setText(text)
        self.__frame_btn.setObjectName("frame_btn")
        self.__frame_btn.setFont(
            QtGui.QFont(QtFonts.SegoeUI, 10, QtGui.QFont.ExtraBold)
        )
        self.__frame_btn.collapsed.add(self.__on_collapsed)
        self.__frame_btn.expanded.add(self.__on_expanded)

        self.__frame = QtWidgets.QWidget(self)
        self.__frame.setObjectName("frame_widget")
        self.__frame.setContentsMargins(3, 3, 3, 3)
        self.__frame.setStyleSheet(
            f"""
            QWidget {{
                border: 1px solid {_hex("272727")};
                border-bottom-right-radius: 12px;
                background-color: {_hex("363636")};
            }}
            """
        )

        self.__frame_layout = QtWidgets.QVBoxLayout(self.__frame)
        self.__frame_layout.setObjectName("frame_layout")
        self.__frame_layout.setContentsMargins(0, 0, 0, 0)
        self.__frame_layout.setSpacing(0)

        self.layout().addWidget(self.__frame_btn)
        self.layout().addWidget(self.__frame)

        # self.frame_btn.toggle = True

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)

    @property
    def frame_btn(self):
        """Access to _FrameButton"""
        return self.__frame_btn

    @property
    def frame_layout(self):
        """Access to Layout section"""
        return self.__frame_layout

    def collapsed(self):
        self.__on_collapsed()

    def __on_collapsed(self):
        """Hide item in layout when _FrameButton is closed"""
        for item in self.__frame.findChildren(QtWidgets.QWidget):
            item.setVisible(getattr(item, "force_visible", False))

    def __on_expanded(self):
        """Show Item in layout when _FrameButton is open"""
        for item in self.__frame.findChildren(QtWidgets.QWidget):
            item.setVisible(getattr(item, "force_visible", True))

    def set_text(self, text):
        """Set the text of _FrameButton"""
        self.__frame_btn.setText(text)

    def set_toggle(self, toggle):
        """Set the toggle of _FrameButton"""
        self.__frame_btn.toggle = toggle


class QtFrameButtonCSWidget(QtDefaultCSWidget):
    """
    Custom QtFrameButton subclass, serves as the button part within QtFrameLayoutWidget
    The open and closed states of QtFrameLayoutWidget are controlled by this button
    """

    def __init__(self, label=None, parent=None, status=None):
        super().__init__(parent)

        self.__close_pix = QtGui.QPixmap(":/teRightArrow.png")
        self.__open_pix = QtGui.QPixmap(":/teDownArrow.png")

        self.setMinimumSize(288, 24)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.setAutoFillBackground(True)

        self.color_default = (39, 39, 39)
        self.color_hover = (46, 46, 46)

        self.setBackgroundColor(self.color_default)  # Dark

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(12)
        layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.__icon = QtWidgets.QLabel()
        self.__icon.setPixmap(self.__close_pix)
        layout.addWidget(self.__icon)
        if label:
            self.__label = QtWidgets.QLabel(" " + label)

        layout.addWidget(self.__label)
        self.setLayout(layout)

        class _Listener(object):
            """Process registration class"""

            def __init__(self, container):
                self.__container = container

            def add(self, func):
                self.__container.append(func)

            def remove(self, func):
                if func in self.__container:
                    self.__container.remove(func)

        class Subject(object):
            """Processing notification class"""

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
        self.__collapsed.listen.add(lambda: self.__icon.setPixmap(self.__close_pix))
        self.__expanded.listen.add(lambda: self.__icon.setPixmap(self.__open_pix))

    @property
    def toggle(self):
        """
        Programmatic processing for status acquisition
        """
        return self.__toggle

    @toggle.setter
    def toggle(self, value):
        """
        Process for programmed state setting
        """
        self.__toggle = value
        self.__expanded.emit() if self.__toggle else self.__collapsed.emit()

    @property
    def collapsed(self):
        """
        Register function when FrameLayout is closed
        """
        return self.__collapsed.listen

    @property
    def expanded(self):
        """
        Register function when a FrameLayout is opened
        """
        return self.__expanded.listen

    def setFont(self, font):
        """
        Font settings
        """
        self.__label.setFont(font)

    def setText(self, text):
        """
        Text settings
        """
        self.__label.setText(text)

    def setBackgroundColor(self, color):
        _p = self.palette()
        _p.setColor(self.backgroundRole(), QtGui.QColor(color[0], color[1], color[2]))
        self.setPalette(_p)

    def mouseReleaseEvent(self, *args, **kwargs):
        """
        FrameLayout button click decision.
        """
        self.__toggle = not self.__toggle
        self.__expanded.emit() if self.__toggle else self.__collapsed.emit()

    def enterEvent(self, *args, **kwargs):
        """
        Mouse enter event
        """
        self.setBackgroundColor(self.color_hover)

    def leaveEvent(self, *args, **kwargs):
        """
        Mouse leave event
        """
        self.setBackgroundColor(self.color_default)


class QtBoxLayoutCSWidget(QtWidgets.QBoxLayout):
    """Custom QBoxLayout subclass"""

    def __init__(self, parent=None):
        super().__init__(parent)

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)


class QtGroupBoxCSWidget(QtWidgets.QGroupBox):
    """Custom QGroupBox subclass"""

    def __init__(self, parent=None, flat=None):
        super().__init__(parent)
        self.force_visible = True

        font = QtGui.QFont(QtFonts.MicrosoftJhengHei, 8, QtGui.QFont.Bold)
        font.setLetterSpacing(QtGui.QFont.PercentageSpacing, 110)
        self.setFont(QtGui.QFont(font))
        if flat:
            self.setFlat(flat)

    def set_force_visible(self, visible):
        self.force_visible = visible
        self.setVisible(visible)

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)


class QtGroupHBoxCSWidget(QtGroupBoxCSWidget):
    """Custom QtGroupHBox subclass"""

    def __init__(
        self,
        parent=None,
        flat=True,
        text=None,
        margin=(6, 24, 6, 6),
        spacing=6,
        status=None,
    ):
        super().__init__(parent, flat)

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(*margin)
        layout.setSpacing(spacing)
        self.setLayout(layout)

        # --------------------------------------------
        self.layout = layout
        self.layout_content: list[QtWidgets] = []  # 存放所有子部件
        # --------------------------------------------

        if text:
            self.setTitle("  " + text + "  ")
        if status:
            self.set_status(status)
        else:
            self.set_status(QtGroupBoxStatus.Default)

    def set_text(self, text):
        self.setTitle("  " + text + "  ")

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)

    def set_status(self, status):
        self.setStyleSheet(status)


class QtGroupVBoxCSWidget(QtGroupBoxCSWidget):
    """Custom QtGroupVBox subclass"""

    def __init__(
        self,
        parent=None,
        flat=True,
        text=None,
        margin=(6, 24, 6, 6),
        spacing=6,
        status=None,
    ):
        super().__init__(parent, flat)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(*margin)
        layout.setSpacing(spacing)
        self.setLayout(layout)

        # --------------------------------------------
        self.force_visible = True
        self.layout = layout
        self.layout_content: list[QtWidgets] = []  # 存放所有子部件
        # --------------------------------------------

        if text:
            self.setTitle("  " + text + "  ")
        if status:
            self.set_status(status)
        else:
            self.set_status(QtGroupBoxStatus.Default)

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)

    def set_status(self, status):
        self.setStyleSheet(status)


class QtInfoBoxCSWidget(QtGroupBoxCSWidget):
    """Custom QtInfoBox subclass"""

    class InfoType:
        Information = ":/info.png"
        Warning = ":/warningIcon.svg"
        Error = ":/error.png"

    def __init__(
        self,
        parent=None,
        flat=True,
        title=None,
        text=None,
        icon=None,
        margin=(0, 0, 0, 0),
        spacing=3,
        width=None,
        height=None,
        status=None,
    ):
        super().__init__(parent, flat)

        self.info_type = self.InfoType()

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(spacing)

        label = QtLabelCSWidget(text)
        font = QtGui.QFont("Microsoft JhengHei", 8, QtGui.QFont.Bold)
        font.setLetterSpacing(QtGui.QFont.PercentageSpacing, 100)
        label.setFont(QtGui.QFont(font))
        label.setWordWrap(True)

        self.pixmap = QtLabelCSWidget()

        if title:
            self.setTitle(title)
        if text:
            label.setText(text)
        if margin:
            layout.setContentsMargins(*margin)
        if status:
            self.set_status(status)
        else:
            self.set_status(QtInfoBoxStatus.Default)
        if icon:
            project_dir = Registry.get_value(
                reg_.REG_KEY, reg_.REG_SUB, "Pref_ModuleProjectDirectory", ""
            )
            icon_filepath = project_dir + qt_.ICON_DIR + icon
            try:
                self.pixmap.setPixmap(QtGui.QPixmap(icon_filepath))
                self.pixmap.setFixedSize(20, 20)
                layout.addWidget(self.pixmap)
            except Exception as e:
                print(e)
        else:
            project_dir = Registry.get_value(
                reg_.REG_KEY, reg_.REG_SUB, "Pref_ModuleProjectDirectory", ""
            )
            icon_dir = project_dir + qt_.ICON_DIR
            icon_filepath = ""
            if status == QtInfoBoxStatus.Info:
                icon_filepath = ":/info.png"
            elif status == QtInfoBoxStatus.Help:
                icon_filepath = ":/help.png"
            elif status == QtInfoBoxStatus.Warning:
                icon_filepath = ":/warningIcon.svg"
            elif status == QtInfoBoxStatus.Error:
                icon_filepath = ":/error.png"
            elif status == QtInfoBoxStatus.Success:
                icon_filepath = icon_dir + "success.png"
            elif status == QtInfoBoxStatus.Disable:
                icon_filepath = ":/RS_disable.png"
            else:
                icon_filepath = ""

            self.pixmap.setPixmap(QtGui.QPixmap(icon_filepath))
            self.pixmap.setFixedSize(20, 20)
            layout.addWidget(self.pixmap)

        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)

        self.set_extra_stylesheet()

        layout.addWidget(label)

        # 設置主要布局
        self.setLayout(layout)

        # 儲存當前的部件
        self.label = label
        self.layout = layout

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)

    def set_status(self, status):
        self.setStyleSheet(status)
        self.set_icon(status)

    def set_extra_stylesheet(self):
        stylesheet = self.styleSheet() + "\n" + QtStylesheet.Tooltip
        self.setStyleSheet(stylesheet)

    def set_icon(self, status):
        project_dir = Registry.get_value(
            reg_.REG_KEY, reg_.REG_SUB, "Pref_ModuleProjectDirectory", ""
        )
        icon_dir = project_dir + qt_.ICON_DIR
        icon_filepath = ""
        if status == QtInfoBoxStatus.Info:
            icon_filepath = ":/info.png"
        elif status == QtInfoBoxStatus.Help:
            icon_filepath = ":/help.png"
        elif status == QtInfoBoxStatus.Warning:
            icon_filepath = ":/warningIcon.svg"
        elif status == QtInfoBoxStatus.Error:
            icon_filepath = ":/error.png"
        elif status == QtInfoBoxStatus.Success:
            icon_filepath = icon_dir + "success.png"
        elif status == QtInfoBoxStatus.Disable:
            icon_filepath = ":/RS_disable.png"
        else:
            icon_filepath = ""

        self.pixmap.setPixmap(QtGui.QPixmap(icon_filepath))


# Molecular Widget
class QtHelperCSWidget(QtLabelCSWidget):
    """Custom QtHelper subclass"""

    def __init__(self, parent=None, text=None, status=None):
        super().__init__(parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.setWordWrap(True)
        if text:
            self.setText(text)
        if status:
            self.set_status(status)
        else:
            self.set_status(QtHelperStatus.Default)

        self.set_extra_stylesheet()

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)

    def set_status(self, status):
        self.setStyleSheet(status)

    def set_extra_stylesheet(self):
        stylesheet = self.styleSheet() + "\n" + QtStylesheet.Tooltip
        self.setStyleSheet(stylesheet)


class LineEditProxy:
    def __init__(self, lineedits):
        self.lineedits = lineedits

    def setReadOnly(self, state):
        for le in self.lineedits:
            le.setReadOnly(state)

    def setText(self, text):
        for le in self.lineedits:
            le.setText(text)

    def setAlignment(self, align):
        for le in self.lineedits:
            le.setAlignment(align)

    def setCursorPosition(self, position):
        for le in self.lineedits:
            le.setCursorPosition(position)

    def setPlaceholderText(self, placeholder):
        for le in self.lineedits:
            le.setPlaceholderText(placeholder)

    def setFixedWidth(self, width):
        for le in self.lineedits:
            le.setFixedWidth(width)

    def setFixedHeight(self, height):
        for le in self.lineedits:
            le.setFixedHeight(height)

    def setStyleSheet(self, stylesheet):
        for le in self.lineedits:
            le.setStyleSheet(stylesheet)


class QtTextLineCSWidget(QtDefaultCSWidget):
    """Custom QtTextLine subclass, contains a label and a read-only text box arranged in a horizontal layout"""

    def __init__(
        self,
        parent=None,
        use_label=True,
        title=None,
        text=None,
        placeholder=None,
        readonly=False,
        align="left",
        spacing=None,
        width=None,
        height=None,
        status=None,
        ratio=0.5,
    ):
        super().__init__(parent)
        self.force_visible = True

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.setLayout(layout)

        # --------------------------------------------
        self.use_label = use_label
        self.real_lineedits = []  # 存放實際的 QtLineEditCSWidget 實例
        self.lineedit = None
        self.layout = layout
        # --------------------------------------------

        if title:
            self.label = QtLabelCSWidget()
            self.label.setFixedWidth(100)
            if title:
                self.label.setText(title)
            font = QtGui.QFont(QtFonts.MicrosoftJhengHei, 8, QtGui.QFont.Bold)
            font.setLetterSpacing(QtGui.QFont.PercentageSpacing, 100)
            self.label.setFont(QtGui.QFont(font))
            self.layout.addWidget(self.label)
        if spacing:
            self.layout.setSpacing(spacing)
        if text or text == "":
            self.create_line_edits(
                text,
                readonly,
                align,
                placeholder,
                width,
                height,
                ratio,
                status,
            )
        if status:
            self.set_status(status)
        else:
            pass

        self.set_extra_stylesheet()

    def set_text(self, text):
        self.create_line_edits(text)

    def create_line_edits(
        self,
        texts,
        readonly=False,
        align="left",
        placeholder=None,
        width=None,
        height=None,
        ratio=0.9,
        status=None,
    ):
        self.real_lineedits.clear()
        if isinstance(texts, str):
            texts = [texts]

        total_texts = len(texts)
        if total_texts <= 1:
            scale_factors = [1] * total_texts  # 避免division by zero
        else:
            scale_factors = [
                (1 - ratio) + (ratio * 2 - 1) * (i / (total_texts - 1))
                for i in range(total_texts)
            ]

        for i, text in enumerate(texts):
            _lineedit = QtLineEditCSWidget()
            _lineedit.setReadOnly(readonly)
            _lineedit.setText(text)

            size_policy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
            )

            scale_factor = 1 - scale_factors[i]
            if width:
                _lineedit.setFixedWidth(int(width * scale_factor))
            else:
                size_policy.setHorizontalStretch(int(100 * scale_factor))  # 設定水平拉伸因子
                _lineedit.setSizePolicy(size_policy)

            self.real_lineedits.append(_lineedit)
            self.layout.addWidget(_lineedit)

        self.lineedit = LineEditProxy(self.real_lineedits)
        if align == "left":
            self.lineedit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        elif align == "center":
            self.lineedit.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        elif align == "right":
            self.lineedit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        if placeholder:
            self.lineedit.setPlaceholderText(placeholder)
        if height:
            self.lineedit.setFixedHeight(height)
        if status:
            self.lineedit.setStyleSheet(status)

        self.lineedit.setCursorPosition(0)

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)

    def set_force_visible(self, visible):
        self.force_visible = visible
        self.setVisible(visible)

    def set_status(self, status):
        self.lineedit.setStyleSheet(status)

    # def set_extra_stylesheet(self):
    #     stylesheet = self.styleSheet() + "\n" + QtStylesheet.Tooltip
    #     self.lineedit.setStyleSheet(stylesheet)


class QtCheckBoxLineCSWidget(QtDefaultCSWidget):
    """Custom QtCheckBoxLine subclass, contains a label and a read-only text box arranged in a horizontal layout"""

    def __init__(self, parent=None, text=None, default_bool=None):
        super().__init__(parent)
        checkbox = QtCheckBoxCSWidget(status=QtCheckBoxStatus.Default)

        label = QtLabelCSWidget()
        # label.setFixedWidth(240)
        label_font = QtGui.QFont(QtFonts.MicrosoftJhengHei, 8, QtGui.QFont.Bold)
        label_font.setLetterSpacing(QtGui.QFont.PercentageSpacing, 100)
        label.setFont(QtGui.QFont(label_font))

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        layout.addWidget(checkbox)
        layout.addWidget(label)

        self.setLayout(layout)

        # --------------------------------------------
        self.checkbox = checkbox
        self.label = label
        self.layout = layout
        # --------------------------------------------

        if text:
            self.label.setText(text)
        if default_bool:
            self.checkbox.setChecked(default_bool)

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)


class QtTreeCSWidget(QtWidgets.QTreeWidget):
    """Custom QtTreeWidget subclass"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        font = QtGui.QFont("Microsoft JhengHei", 8)
        font.setLetterSpacing(QtGui.QFont.PercentageSpacing, 100)
        self.setFont(QtGui.QFont(font))

        self.current_item: QtTreeItemCSWidget = self.currentItem()

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)

    def set_status(self, status):
        self.setStyleSheet(status)

    def set_extra_stylesheet(self):
        stylesheet = self.styleSheet() + "\n" + QtStylesheet.Tooltip
        self.setStyleSheet(stylesheet)


class QtTreeItemCSWidget(QtWidgets.QTreeWidgetItem):
    """Custom QtTreeItem subclass"""

    class Status:
        Normal = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0), QtCore.Qt.NoBrush)
        Changed = QtGui.QBrush(QtGui.QColor("#5d5335"))
        Override = QtGui.QBrush(QtGui.QColor("#5D4935"))
        Missing = QtGui.QBrush(QtGui.QColor("#5d3535"))

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tree: QtTreeCSWidget = QtTreeCSWidget()

        self.matched_path = ""

        self.status = self.Status()
        self.current_status = self.status.Normal

    def set_status(self, status):
        if status == self.Status.Normal:
            self.set_background(self.Status.Normal)
            self.current_status = self.status.Normal
            self.setText(1, self.matched_path)

        if status == self.Status.Changed:
            self.set_background(self.Status.Changed)
            self.current_status = self.status.Changed

        if status == self.Status.Override:
            self.set_background(self.Status.Override)
            self.current_status = self.status.Override

        if status == self.Status.Missing:
            self.set_background(self.Status.Missing)
            self.current_status = self.status.Missing
            self.setText(1, "找不到路徑")

    def set_background(self, brush):
        for colum in range(0, self.columnCount()):
            self.setBackground(colum, brush)


# Element Widget
class QtSpacerCSWidget(QtWidgets.QSpacerItem):
    """Custom QtSpacer subclass"""

    def __init__(
        self,
        size_h=20,
        size_v=40,
        policy_h=QtWidgets.QSizePolicy.Minimum,
        policy_v=QtWidgets.QSizePolicy.Expanding,
        *args,
        **kwargs,
    ):
        super().__init__(size_h, size_v, policy_h, policy_v, *args, **kwargs)


class QtLineCSWidget(QtWidgets.QFrame):
    """Custom QFrame subclass, for decorative lines"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame().HLine)
        self.setFrameShadow(QtWidgets.QFrame().Raised)

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)


# Widget Status


def _hex(h):
    return "#" + h


class QtStylesheet:
    Tooltip = f"""
        QToolTip {{
            background-color: {_hex("282828")};
            color: {_hex("ADD8E6")};
            border: 1px solid {_hex("1E90FF")};
            padding: 2px;
        }}
    """


class QtLabelStatus:
    Default = f"""
        QLabel {{
            color: {_hex("B0B0B0")};
            border: None;
            background-color: None;
        }}
    """
    Info = f"""
        QLabel {{
            color: {_hex("A6D8FF")};
        }}
    """
    Warning = f"""
        QLabel {{
            color: {_hex("FFEB8A")};
        }}
    """

    Error = f"""
        QLabel {{
            color: {_hex("FF8F76")};
        }}
    """

    Verified = f"""
        QLabel {{
            color: {_hex("C5F2C5")};
        }}
    """

    Disabled = f"""
        QLabel {{
            color: {_hex("636363")};
        }}
    """


class QtLineEditStatus:
    Default = f"""
        QLineEdit {{
            background-color: {_hex("1d1d1d")};
            border: 2px solid {_hex("444444")};
            color: {_hex("B0B0B0")};
        }}
        QLineEdit:focus {{
            border: 2px solid {_hex("606060")};
        }}
        QLineEdit:hover {{
            border: 2px solid {_hex("606060")};
        }}
    """

    Info = f"""
        QLineEdit {{
            background-color: {_hex("1d1d1d")};
            border: 2px solid {_hex("1E90FF")};
            color: {_hex("A6D8FF")};
        }}
        QLineEdit:focus {{
            border: 2px solid {_hex("A6D8FF")};
        }}
        QLineEdit:hover {{
            border: 2px solid {_hex("A6D8FF")};
        }}
    """
    Warning = f"""
        QLineEdit {{
            background-color: {_hex("1d1d1d")};
            border: 2px solid {_hex("8E6D37")};
            color: {_hex("FFEB8A")};
        }}
        QLineEdit:focus {{
            border: 2px solid {_hex("FFEB8A")};
        }}
        QLineEdit:hover {{
            border: 2px solid {_hex("FFEB8A")};
        }}
    """

    Error = f"""
        QLineEdit {{
            background-color: {_hex("1d1d1d")};
            border: 2px solid {_hex("8E3B2E")};
            color: {_hex("FF8F76")};
        }}
        QLineEdit:focus {{
            border: 2px solid {_hex("FF8F76")};
        }}
        QLineEdit:hover {{
            border: 2px solid {_hex("FF8F76")};
        }}
    """

    Success = f"""
        QLineEdit {{
            background-color: {_hex("1d1d1d")};
            border: 2px solid {_hex("348E34")};
            color: {_hex("C5F2C5")};
        }}
        QLineEdit:focus {{
            border: 2px solid {_hex("C5F2C5")};
        }}
        QLineEdit:hover {{
            border: 2px solid {_hex("C5F2C5")};
        }}
    """

    Disable = f"""
        QLineEdit {{
            background-color: {_hex("1d1d1d")};
            border: 2px solid {_hex("3c3c3c")};
            color: {_hex("636363")};
        }}
        QLineEdit:focus {{
            border: 2px solid {_hex("636363")};
        }}
        QLineEdit:hover {{
            border: 2px solid {_hex("636363")};
        }}
    """


class QtCheckBoxStatus:
    project_dir = Registry.get_value(
        reg_.REG_KEY, reg_.REG_SUB, "Pref_ModuleProjectDirectory", ""
    )
    icon_filepath = project_dir + qt_.ICON_DIR + "so-checkmark.svg"

    Default = f"""
        QCheckBox {{
            color: {_hex("1E90FF")};
            padding: 5px;
        }}

        QCheckBox::indicator {{
            width: 13px;
            height: 13px;
        }}

        QCheckBox::indicator:unchecked {{
            background-color: {_hex("444444")};
            border: 2px solid {_hex("1E90FF")};
        }}

        QCheckBox::indicator:checked {{
            background-color: {_hex("1E90FF")};
            border: 2px solid {_hex("1E90FF")};
            image: url({icon_filepath});
        }}

        QCheckBox:hover {{
            color: {_hex("ADD8E6")};
        }}

        QCheckBox::indicator:hover {{
            border-color: {_hex("ADD8E6")};
        }}
    """


class QtButtonStatus:
    Default = f"""
            QPushButton {{
                color: {_hex("bdbdbd")};
                border: 1px solid {_hex("606060")};
                background-color: {_hex("525252")};
                padding-left: 6px;
                padding-right: 6px;
                padding-top: 3px;
                padding-bottom: 3px;
                outline: none;
                text-align: center;
            }}

            QPushButton:hover {{
                border: 1px solid {_hex("B0B0B0")};
            }}
            QPushButton:pressed {{
                background-color: {_hex("707070")};
            }}
        """

    Invert = f"""
            QPushButton {{
                border: 2px solid {_hex("1E90FF")};
                background-color: {_hex("333333")};
                color: {_hex("1E90FF")};
                padding-left: 6px;
                padding-right: 6px;
                padding-top: 3px;
                padding-bottom: 3px;
                outline: none;
                text-align: center;
            }}

            QPushButton:hover {{
                background-color: {_hex("1E90FF")};
                color: {_hex("333333")};
            }}

            QPushButton:pressed {{
                background-color: {_hex("104E8B")};
                color: {_hex("63b2ff")};
            }}
        """
    Info = f"""
            QPushButton {{
                color: {_hex("bdbdbd")};
                border: 1px solid {_hex("B0B0B0")};
                background-color: {_hex("525252")};
                padding-left: 6px;
                padding-right: 6px;
                padding-top: 3px;
                padding-bottom: 3px;
                outline: none;
                text-align: center;
            }}

            QPushButton:hover {{
                border: 1px solid {_hex("B0B0B0")};
            }}
            QPushButton:pressed {{
                background-color: {_hex("707070")};
            }}
            """
    Help = f"""
            QPushButton {{
                color: {_hex("bdbdbd")};
                border: 1px solid {_hex("1E90FF")};
                background-color: {_hex("3c3c3c")};
                padding-left: 6px;
                padding-right: 6px;
                padding-top: 3px;
                padding-bottom: 3px;
                outline: none;
                text-align: center;
            }}

            QPushButton:hover {{
                border: 1px solid {_hex("B0B0B0")};
            }}
            QPushButton:pressed {{
                background-color: {_hex("707070")};
            }}
            """
    Warning = f"""
            QPushButton {{
                color: {_hex("bdbdbd")};
                border: 1px solid {_hex("fbb549")};
                background-color: {_hex("3e3527")};
                padding-left: 6px;
                padding-right: 6px;
                padding-top: 3px;
                padding-bottom: 3px;
                outline: none;
                text-align: center;
            }}

            QPushButton:hover {{
                border: 1px solid {_hex("B0B0B0")};
            }}
            QPushButton:pressed {{
                background-color: {_hex("707070")};
            }}
            """

    Error = f"""
            QPushButton {{
                color: {_hex("bdbdbd")};
                border: 1px solid {_hex("cf3539")};
                background-color: {_hex("5d3535")};
                padding-left: 6px;
                padding-right: 6px;
                padding-top: 3px;
                padding-bottom: 3px;
                outline: none;
                text-align: center;
            }}

            QPushButton:hover {{
                border: 1px solid {_hex("B0B0B0")};
            }}
            QPushButton:pressed {{
                background-color: {_hex("707070")};
            }}
            """

    Success = f"""
            QPushButton {{
                color: {_hex("bdbdbd")};
                border: 1px solid {_hex("348E34")};
                background-color: {_hex("174117")};
                padding-left: 6px;
                padding-right: 6px;
                padding-top: 3px;
                padding-bottom: 3px;
                outline: none;
                text-align: center;
            }}

            QPushButton:hover {{
                border: 1px solid {_hex("B0B0B0")};
            }}
            QPushButton:pressed {{
                background-color: {_hex("707070")};
            }}
            """

    Disable = f"""
            QPushButton {{
                color: {_hex("bdbdbd")};
                border: 1px solid {_hex("000000")};
                background-color: {_hex("2b2b2b")};
                padding-left: 6px;
                padding-right: 6px;
                padding-top: 3px;
                padding-bottom: 3px;
                outline: none;
                text-align: center;
            }}

            QPushButton:hover {{
                border: 1px solid {_hex("B0B0B0")};
            }}
            QPushButton:pressed {{
                background-color: {_hex("707070")};
            }}
            """
    Invisible = f"""
            QPushButton {{
                border: 1px solid {_hex("3c3c3c")};
                background-color: transparent;
                color: transparent;
                padding-left: 6px;
                padding-right: 6px;
                padding-top: 3px;
                padding-bottom: 3px;
                outline: none;
                text-align: center;
            }}
        """


class QtGroupBoxStatus:
    Default = f"""
            QGroupBox {{
                background-color: {_hex("3c3c3c")};
                border: 1px solid {_hex("444444")};
            }}

            QGroupBox::title {{
                color: {_hex("bdbdbd")};
                background-color: {_hex("2b2b2b")};
                border-bottom-right-radius: 6px;
            }}
        """
    Invert = f"""
            QGroupBox {{
                background-color: {_hex("333333")};
                border: 1px solid {_hex("1460aa")};
            }}

            QGroupBox::title {{
                color: {_hex("1e90ff")};
                background-color: {_hex("282828")};
            }}
        """
    Borderless = f"""
            QGroupBox {{
                background-color: {_hex("444444")};
                border: 0px;
            }}

            QGroupBox::title {{
                color: {_hex("282828")};
                background-color: {_hex("1e90ff")};
            }}
        """
    Borderless_Invert = f"""
            QGroupBox {{
                background-color: {_hex("3c3c3c")};
                border: 0px;
            }}

            QGroupBox::title {{
                color: {_hex("1e90ff")};
                background-color: {_hex("282828")};
            }}
        """
    Border = f"""
                QGroupBox {{
                background-color: None;
                border: 0px;
            }}

            QGroupBox::title {{
                color: None;
                background-color: None;
            }}
    """
    Disabled = f"""
            QGroupBox {{
                background-color: {_hex("3c3c3c")};
                border: 1px solid {_hex("282828")};
            }}

            QGroupBox::title {{
                color: {_hex("282828")};
                background-color: {_hex("636363")};
            }}
        """
    Disabled_Invert = f"""
            QGroupBox {{
                background-color: {_hex("3c3c3c")};
                border: 1px solid {_hex("282828")};
            }}

            QGroupBox::title {{
                color: {_hex("636363")};
                background-color: {_hex("282828")};
            }}
        """


class QtInfoBoxStatus:
    Default = f"""
            QGroupBox {{
                background-color: {_hex("3c3c3c")};
                border: 1px solid {_hex("444444")};
                border-radius: 4px;
                padding: 3px;
            }}
            """
    Info = f"""
            QGroupBox {{
                background-color: {_hex("525252")};
                border: 1px solid {_hex("B0B0B0")};
                border-radius: 4px;
                padding: 3px;
            }}
            """
    Help = f"""
            QGroupBox {{
                background-color: {_hex("3c3c3c")};
                border: 1px solid {_hex("1E90FF")};
                border-radius: 4px;
                padding: 3px;
            }}
            """
    Warning = f"""
            QGroupBox {{
                background-color: {_hex("3e3527")};
                border: 1px solid {_hex("fbb549")};
                border-radius: 4px;
                padding: 3px;
                
            }}
            """

    Error = f"""
            QGroupBox {{
                background-color: {_hex("5d3535")};
                border: 1px solid {_hex("cf3539")};
                border-radius: 4px;
                padding: 3px;
            }}
            """

    Success = f"""
            QGroupBox {{
                background-color: {_hex("174117")};
                border: 1px solid {_hex("348E34")};
                border-radius: 4px;
                padding: 3px;
            }}
            """

    Disable = f"""
            QGroupBox {{
                background-color: {_hex("2b2b2b")};
                border: 1px solid {_hex("000000")};
                border-radius: 4px;
                padding: 3px;
            }}
            """


class QtHelperStatus:
    Default = f"""
            QLabel {{
                color: {_hex("B0B0B0")};
                background-color: {_hex("4d4d4d")};
                border: 1px solid {_hex("3c3c3c")};
                border-radius: 4px;
                padding: 3px;
            }}
            """

    Info = f"""
            QLabel {{
                color: {_hex("A6D8FF")};
                background-color: {_hex("3c3c3c")};
                border: 1px solid {_hex("1E90FF")};
                border-radius: 4px;
                padding: 3px;
            }}
            """

    Warning = f"""
            QLabel {{
                color: {_hex("FFEB8A")};
                background-color: {_hex("8E6D37")};
                border: 1px solid {_hex("333333")};
                border-radius: 4px;
                padding: 3px;
            }}
            """

    Error = f"""
            QLabel {{
                color: {_hex("FF8F76")};
                background-color: {_hex("8E3B2E")};
                border: 1px solid {_hex("333333")};
                border-radius: 4px;
                padding: 3px;
            }}
            """

    Verified = f"""
            QLabel {{
                color: {_hex("C5F2C5")};
                background-color: {_hex("348E34")};
                border: 1px solid {_hex("333333")};
                border-radius: 4px;
                padding: 3px;
            }}
            """

    Disabled = f"""
            QLabel {{
                color: {_hex("636363")};
                background-color: {_hex("3c3c3c")};
                border: 1px solid {_hex("333333")};
                border-radius: 4px;
                padding: 3px;
            }}
            """
