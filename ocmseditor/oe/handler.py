from dataclasses import dataclass

from ocmseditor.tool.maya import Maya
from ocmseditor.tool.registry import Registry
from ocmseditor.oe.constant import REG_MAYA_JOB_IDS
from ocmseditor.oe.utils.qt import QtCore, QtGui
from ocmseditor.oe.repository import RepositoryFacade


class EventHandler:
    """Singleton"""

    _instance = None
    subscribers = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventHandler, cls).__new__(cls)
        return cls._instance

    @classmethod
    def subscribe(cls, event_name, callback):
        cls.subscribers.setdefault(event_name, [])
        cls.subscribers[event_name].append(callback)

    @classmethod
    def unsubscribe(cls, event_name, callback):
        if event_name in cls.subscribers:
            cls.subscribers[event_name].remove(callback)

    @classmethod
    def call(cls, event_name):
        for callback in cls.subscribers.get(event_name, []):
            callback()


@dataclass
class SelectionChangedEvent:
    is_fired: bool = False


def subscribe_events():
    EventHandler.subscribe("on_selection_changed", lambda: fetch_active_object())
    EventHandler.subscribe(
        "on_selection_changed", lambda: update_edit_attribute_delay()
    )


def fetch_active_object():
    maya = RepositoryFacade().maya
    if len(Maya.get_active_object()) != 0:
        maya.active_object = Maya.get_active_object()[0]


def fetch_active_viewport():
    maya = RepositoryFacade().maya
    maya.active_viewport = Maya.get_active_viewport()


def update_edit_attribute():
    from ocmseditor.oe.module.attribute.ui import EditAttributeWidget

    fetch_active_viewport()
    maya = RepositoryFacade().maya
    geom = maya.active_viewport.geometry()
    global_point = maya.active_viewport.mapToGlobal(geom.topLeft())
    modified_point = QtCore.QPoint(global_point.x() + 2, global_point.y() + 40)
    edit_attribute = RepositoryFacade().ui.edit_attribute
    edit_attribute: EditAttributeWidget
    edit_attribute.edit_attribute.move(modified_point)
    context = {}
    maya = RepositoryFacade().maya
    attrs = Maya.get_attrs(maya.active_object)
    edit_attribute.redraw_met_edit_panel(attrs)


def update_edit_attribute_delay():
    QtCore.QTimer.singleShot(100, update_edit_attribute)


def add_maya_selection_changed_script_job():
    job_id_str = Registry.get(REG_MAYA_JOB_IDS)
    job_id_list = list(
        map(int, filter(lambda ids: ids != "" and ids != "None", job_id_str.split(",")))
    )
    job_id_list.append(
        Maya.add_script_job(
            event=[
                "SelectionChanged",
                lambda: EventHandler.call("on_selection_changed"),
            ]
        )
    )
    job_id_str = ",".join(map(str, job_id_list))
    Registry.set(REG_MAYA_JOB_IDS, job_id_str)


def del_maya_selection_changed_script_job():
    job_id_str = Registry.get(REG_MAYA_JOB_IDS)
    job_id_list = list(
        map(int, filter(lambda ids: ids != "" and ids != "None", job_id_str.split(",")))
    )
    while job_id_list:
        job_id = job_id_list.pop()
        Maya.del_script_job(kill=job_id, force=True)

    job_id_str = ",".join(map(str, job_id_list))
    Registry.set(REG_MAYA_JOB_IDS, job_id_str)
