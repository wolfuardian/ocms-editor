from ocmseditor.tool.maya import Maya
from ocmseditor.oe.repository import RepositoryFacade
def op_set_attr(obj_name, long_name, value):
    print(f"obj_name: {obj_name}, long_name: {long_name}, value: {value}")
    pass
    # tool.Maya.set_string_attr(long_name, value, obj_name)


def op_fetch_attrs():
    context = {}
    maya = RepositoryFacade().maya
    attrs = Maya.get_attrs(maya.active_object)
    context.update({"attrs": attrs})
    __ui = ocms.ui.context.get("frame_edit_attr")
    if __ui:
        __ui.redraw_met_edit_panel(context)