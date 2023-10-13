from dataclasses import dataclass, field
from ocmseditor.oe.utils.qt import QtWidgets


class Repository:
    """Singleton"""

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Repository, cls).__new__(cls)
            cls.__instance.ui = _UIWidgetDB()
            cls.__instance.ma = _MASceneDB()
            cls.__instance.et = _OCMSElementTreeDB()
            cls.__instance.rs = _OCMSResourceDB()
        return cls.__instance


# class _UIWidgetDB:
#     frame_widgets = []


@dataclass
class _UIWidgetDB:
    main: QtWidgets.QWidget = field(default=None)
    # frame_edit_attribute: QtWidgets.QWidget = field(default=None)
    # frame_other_attribute: QtWidgets.QWidget = field(default=None)


class _MASceneDB:
    pass


class _OCMSElementTreeDB:
    pass


class _OCMSResourceDB:
    pass
