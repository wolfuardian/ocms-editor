from ocmseditor.tool.maya import Maya
from ocmseditor.oe.repository import RepositoryFacade
def op_set_attr(obj_name, attr, attr_value):
    print(f"obj_name: {obj_name}, long_name: {attr}, value: {attr_value}")
    Maya.set_attr(obj_name, attr, attr_value)


def op_fetch_attrs():
    context = {}
    maya = RepositoryFacade().maya
    attrs = Maya.get_attrs(maya.active_object)
    context.update({"attrs": attrs})
    __ui = ocms.ui.context.get("frame_edit_attr")
    if __ui:
        __ui.redraw_edit_attributes(context)