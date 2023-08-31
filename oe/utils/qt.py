from PySide2 import QtWidgets, QtCore, QtGui
from oe.utils.registry import Registry


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
        self.force_visible = True

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.set_extra_stylesheet()

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

        font = QtGui.QFont(QtFonts.MingLiU, 8, QtGui.QFont.Bold)
        self.setFont(font)

        if icon:
            project_dir = Registry.get_value(
                "Software", "MayaBIM", "Pref_ModuleProjectDirectory", ""
            )
            icon_filepath = project_dir + "/mayabim/utils/resources/" + icon
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
    """Custom QScrollArea subclass"""

    def __init__(self, parent=None, margin=(12, 12, 12, 12), spacing=6):
        super().__init__(parent)
        self.force_visible = True

        self.setWidgetResizable(True)

        widget = QtDefaultCSWidget()

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(*margin)
        layout.setSpacing(spacing)

        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setAlignment(QtCore.Qt.AlignTop)

        layout.addLayout(content_layout)

        widget.setLayout(layout)

        self.setWidget(widget)

        # --------------------------------------------
        self.layout = content_layout
        # --------------------------------------------

    def set_force_visible(self, visible):
        self.force_visible = visible
        self.setVisible(visible)

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
        # self.setMinimumSize(width, height)

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

        self.__frame_layout = QtWidgets.QVBoxLayout(self.__frame)
        self.__frame_layout.setObjectName("frame_layout")
        self.__frame_layout.setContentsMargins(0, 0, 0, 0)
        self.__frame_layout.setSpacing(0)

        self.layout().addWidget(self.__frame_btn)
        self.layout().addWidget(self.__frame)

        self.frame_btn.toggle = True

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

        # self.setBackgroundColor((93, 93, 93))  # Light
        self.setBackgroundColor((60, 60, 60))  # Dark
        # self.setBackgroundColor((47, 79, 79))  # Dark

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(12)
        layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.setLayout(layout)

        self.__icon = QtWidgets.QLabel()
        self.__icon.setPixmap(self.__close_pix)
        layout.addWidget(self.__icon)
        if label:
            self.__label = QtWidgets.QLabel(" " + label)

        layout.addWidget(self.__label)

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
        margin=(12, 12, 12, 12),
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
        margin=(12, 12, 12, 12),
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


# Molecular Widget
class QtHelperCSWidget(QtLabelCSWidget):
    """Custom QtHelper subclass"""

    def __init__(self, parent=None, text=None, status=None):
        super().__init__(parent)

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


class QtTextLineCSWidget(QtDefaultCSWidget):
    """Custom QtTextLine subclass, contains a label and a read-only text box arranged in a horizontal layout"""

    def __init__(
        self,
        parent=None,
        use_label=True,
        text=None,
        default=None,
        placeholder=None,
        readonly=False,
        align="left",
        spacing=None,
        width=None,
        height=None,
    ):
        super().__init__(parent)
        lineedit = QtLineEditCSWidget()
        lineedit.setReadOnly(readonly)
        lineedit.setPlaceholderText(">")
        lineedit_font = QtGui.QFont(QtFonts.MicrosoftJhengHei, 8, QtGui.QFont.Bold)
        lineedit_font.setLetterSpacing(QtGui.QFont.PercentageSpacing, 95)
        lineedit.setFont(QtGui.QFont(lineedit_font))
        lineedit.setCursorPosition(0)

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.setLayout(layout)

        # --------------------------------------------
        self.use_label = use_label
        self.lineedit = lineedit
        self.layout = layout
        # --------------------------------------------

        if use_label:
            self.label = QtLabelCSWidget()
            if text:
                self.label.setText(text)
            font = QtGui.QFont(QtFonts.MicrosoftJhengHei, 8, QtGui.QFont.Bold)
            font.setLetterSpacing(QtGui.QFont.PercentageSpacing, 100)
            self.label.setFont(QtGui.QFont(font))
            self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineedit)
        if spacing:
            self.layout.setSpacing(spacing)
        if default:
            self.lineedit.setText(default)
        if align == "left":
            self.lineedit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        elif align == "center":
            self.lineedit.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        elif align == "right":
            self.lineedit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        if placeholder:
            self.lineedit.setPlaceholderText(placeholder)
        if width:
            self.lineedit.setFixedWidth(width)
        if height:
            self.lineedit.setFixedHeight(height)

    def add_to(self, parent):
        parent.addWidget(self)
        return self

    def remove_from(self, parent):
        self.setParent(None)
        parent.removeWidget(self)


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


# Widget Status


def _hex(h):
    return "#" + h


class QtStylesheet:
    Tooltip = f"""
        QToolTip {{
            background-color: {_hex("282828")};
            color: {_hex("ADD8E6")};
            border: 1px solid {_hex("1E90FF")};
            border-radius: 4px;
            padding: 2px;
        }}
    """


class QtLabelStatus:
    Default = f"""
        QLabel {{
            color: {_hex("B0B0B0")};
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
            border: 2px solid {_hex("636363")};
            border-radius: 4px;
            color: {_hex("B0B0B0")};
        }}
        QLineEdit:focus {{
            border: 2px solid {_hex("B0B0B0")};
        }}
    """

    Info = f"""
        QLineEdit {{
            background-color: {_hex("1d1d1d")};
            border: 2px solid {_hex("1E90FF")};
            border-radius: 4px;
            color: {_hex("A6D8FF")};
        }}
        QLineEdit:focus {{
            border: 2px solid {_hex("A6D8FF")};
        }}
    """
    Warning = f"""
        QLineEdit {{
            background-color: {_hex("1d1d1d")};
            border: 2px solid {_hex("8E6D37")};
            border-radius: 4px;
            color: {_hex("FFEB8A")};
        }}
        QLineEdit:focus {{
            border: 2px solid {_hex("FFEB8A")};
        }}
    """

    Error = f"""
        QLineEdit {{
            background-color: {_hex("1d1d1d")};
            border: 2px solid {_hex("8E3B2E")};
            border-radius: 4px;
            color: {_hex("FF8F76")};
        }}
        QLineEdit:focus {{
            border: 2px solid {_hex("FF8F76")};
        }}
    """

    Verified = f"""
        QLineEdit {{
            background-color: {_hex("1d1d1d")};
            border: 2px solid {_hex("348E34")};
            border-radius: 4px;
            color: {_hex("C5F2C5")};
        }}
        QLineEdit:focus {{
            border: 2px solid {_hex("C5F2C5")};
        }}
    """

    Disabled = f"""
        QLineEdit {{
            background-color: {_hex("1d1d1d")};
            border: 2px solid {_hex("3c3c3c")};
            border-radius: 4px;
            color: {_hex("636363")};
        }}
        QLineEdit:focus {{
            border: 2px solid {_hex("636363")};
        }}
    """


class QtCheckBoxStatus:
    project_dir = Registry.get_value(
        "Software", "MayaBIM", "Pref_ModuleProjectDirectory", ""
    )
    icon_filepath = project_dir + "/mayabim/utils/resources/" + "so-checkmark.svg"

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
            border-radius: 4px;
        }}

        QCheckBox::indicator:checked {{
            background-color: {_hex("1E90FF")};
            border: 2px solid {_hex("1E90FF")};
            border-radius: 4px;
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
                border: 2px solid {_hex("444444")};
                border-radius: 4px;
                background-color: {_hex("1E90FF")};
                color: {_hex("333333")};
                padding-left: 6px;
                padding-right: 6px;
                padding-top: 3px;
                padding-bottom: 3px;
                outline: none;
                text-align: center;
            }}

            QPushButton:hover {{
                background-color: {_hex("63b2ff")};
                color: {_hex("333333")};
            }}

            QPushButton:pressed {{
                background-color: {_hex("333333")};
                color: {_hex("1E90FF")};
            }}
        """

    Invert = f"""
            QPushButton {{
                border: 2px solid {_hex("1E90FF")};
                border-radius: 4px;
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


class QtGroupBoxStatus:
    Default = f"""
            QGroupBox {{
                background-color: {_hex("404040")};
                border: 1px solid {_hex("3c3c3c")};
                border-radius: 4px;
            }}

            QGroupBox::title {{
                color: {_hex("282828")};
                background-color: {_hex("1e90ff")};
            }}
        """
    Invert = f"""
            QGroupBox {{
                background-color: {_hex("333333")};
                border: 1px solid {_hex("1460aa")};
                border-radius: 4px;
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
                border-radius: 4px;
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
                border-radius: 4px;
            }}

            QGroupBox::title {{
                color: {_hex("1e90ff")};
                background-color: {_hex("282828")};
            }}
        """
    Disabled = f"""
            QGroupBox {{
                background-color: {_hex("3c3c3c")};
                border: 1px solid {_hex("282828")};
                border-radius: 4px;
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
                border-radius: 4px;
            }}

            QGroupBox::title {{
                color: {_hex("636363")};
                background-color: {_hex("282828")};
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
