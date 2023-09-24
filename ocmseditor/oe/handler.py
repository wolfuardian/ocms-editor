import maya.cmds as cmds

import ocmseditor.tool as tool
import ocmseditor.oe.data.const as const


class EventHub:
    """
    Singleton (單例)
    """

    _instance = None
    subscribers = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventHub, cls).__new__(cls)
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


def create_script_job():
    job_id_str = tool.Registry.get_reg(const.REG_MAYA_JOB_IDS)
    job_id_list = list(map(int, filter(lambda x: x != "", job_id_str.split(","))))

    job_id_list.append(
        cmds.scriptJob(
            event=[
                "SelectionChanged",
                lambda: EventHub.call("on_maya_selection_changed"),
            ]
        )
    )
    # job_id_list.append(cmds.scriptJob(event=["NameChanged", EventHub.call("on_maya_selection_changed")]))

    job_id_str = ",".join(map(str, job_id_list))
    tool.Registry.set_reg(const.REG_MAYA_JOB_IDS, job_id_str)


def delete_script_job():
    job_id_str = tool.Registry.get_reg(const.REG_MAYA_JOB_IDS)
    job_id_list = list(map(int, filter(lambda x: x != "", job_id_str.split(","))))

    while job_id_list:
        job_id = job_id_list.pop()
        cmds.scriptJob(kill=job_id, force=True)

    job_id_str = ",".join(map(str, job_id_list))
    tool.Registry.set_reg(const.REG_MAYA_JOB_IDS, job_id_str)


delete_script_job()
