from ocmseditor.oe.constant import OCMSEDITOR_ROOT


def _hex(h):
    return "#" + h


class QtStyle:
    Tooltip = f"""
        QToolTip {{
            background-color: {_hex("282828")};
            color: {_hex("ADD8E6")};
            border: 1px solid {_hex("1E90FF")};
            padding: 2px;
        }}
    """

    Frame = f"""
    QWidget {{
        border: 1px solid {_hex("272727")};
        border-bottom-right-radius: 12px;
        background-color: {_hex("363636")};
    }}
    """

    Scrollarea = f"""
    QScrollArea {{
        border: None;
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
            background-color: {_hex("2d2d2d")};
            border: 2px solid {_hex("808080")};
            color: {_hex("E1E1E1")};
        }}
        QLineEdit:focus {{
            border: 2px solid {_hex("D0D0D0")};
        }}
        QLineEdit:hover {{
            border: 2px solid {_hex("D0D0D0")};
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
    icon_filepath = OCMSEDITOR_ROOT / "so-checkmark.svg"

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


class QtButtonStyle:
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
            QPushButton:disabled {{
                color: {_hex("636363")};
                border: 1px solid {_hex("3c3c3c")};
                background-color: {_hex("2b2b2b")};
            }}
        """
    Transparent = f"""
            QPushButton {{
                color: {_hex("bdbdbd")};
                border: 1px solid transparent;
                background-color: transparent;
                border-bottom-right-radius: 0px;
            }}

            QPushButton:hover {{
                border: 1px solid {_hex("B0B0B0")};
            }}
            QPushButton:pressed {{
                background-color: {_hex("707070")};
            }}
            QPushButton:disabled {{
                color: {_hex("636363")};
                border: 1px solid {_hex("3c3c3c")};
                background-color: {_hex("2b2b2b")};
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
            QPushButton:disabled {{
                color: {_hex("636363")};
                border: 1px solid {_hex("3c3c3c")};
                background-color: {_hex("2b2b2b")};
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
                border: 1px solid {_hex("060606")};
                background-color: {_hex("2b2b2b")};
                padding-left: 6px;
                padding-right: 6px;
                padding-top: 3px;
                padding-bottom: 3px;
                outline: none;
                text-align: center;
            }}

            QPushButton:hover {{
                border: 1px solid {_hex("202020")};
                background-color: {_hex("333333")};
            }}
            QPushButton:pressed {{
                background-color: {_hex("707070")};
            }}
            QPushButton:disabled {{
                color: {_hex("636363")};
                border: 1px solid {_hex("3c3c3c")};
                background-color: {_hex("2b2b2b")};
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
    Transparent = f"""
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
