from ocmseditor.tool.maya import Maya
from ocmseditor.oe.repository import RepositoryFacade


def op_rename_attr(node, long_name, new_long_name, new_nice_name=""):
    attr_value = Maya.get_attr(node, long_name)
    if not attr_value:
        attr_value = ""
    op_del_attr(node, long_name)
    op_add_attr(
        node=node,
        long_name=new_long_name,
        nice_name=new_nice_name,
        default_value=attr_value,
    )


def op_add_attr(node, long_name, nice_name="", default_value=""):
    Maya.add_attr(
        node=node,
        long_name=long_name,
        nice_name=nice_name,
        default_value=default_value,
    )


def op_del_attr(node, attr):
    Maya.del_attr(node, attr)


def op_set_attr_prop(node, attr, attr_value):
    Maya.set_attr(node, attr, attr_value)


def op_del_attr(node, attr):
    Maya.del_attr(node, attr)
    Maya.select(node)
