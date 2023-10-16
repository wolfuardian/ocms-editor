from dataclasses import dataclass, field
from ocmseditor.oe.utils.qt import QtWidgets


class RepositoryFacade:
    """Singleton"""

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(RepositoryFacade, cls).__new__(cls)
            cls.__instance.ui = _UIWidgetDB()
            cls.__instance.maya = _MASceneDB()
            cls.__instance.ocms = _OCMSElementTreeDB()
            cls.__instance.resource = _OCMSResourceDB()
        return cls.__instance


# class _UIWidgetDB:
#     frame_widgets = []


@dataclass
class _UIWidgetDB:
    main: QtWidgets.QWidget = field(default=None)
    # frame_edit_attribute: QtWidgets.QWidget = field(default=None)
    # frame_other_attribute: QtWidgets.QWidget = field(default=None)


@dataclass
class _MASceneDB:
    active_object: str = field(default=None)


class _OCMSElementTreeDB:
    pass


class _OCMSResourceDB:
    pass
