from ocmseditor.tool.maya import Maya
from ocmseditor.oe.repository import RepositoryFacade


def op_set_attr_name(node, attr, new_attr):
    maya = RepositoryFacade().maya
    attr_value = Maya.get_attr(node, attr)
    if not attr_value:
        attr_value = ""
    Maya.del_attr(node, attr)
    # Maya.add_attr(node, new_attr, default_value=attr_value)
    Maya.select(maya.selected_object)


def op_set_attr_prop(node, attr, attr_value):
    Maya.set_attr(node, attr, attr_value)


def op_del_attr(node, attr):
    Maya.del_attr(node, attr)
    Maya.select(node)

