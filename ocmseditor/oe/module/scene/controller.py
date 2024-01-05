from ocmseditor.tool.maya import Maya
from ocmseditor.oe.repository import RepositoryFacade


class SceneController:
    maya = RepositoryFacade().maya

    @classmethod
    def update_selection(cls):
        cls.maya.selected_object = (
            Maya.get_selected_object()[0] if Maya.get_selected_object() else None
        )
