from ocmseditor.tool.maya import Maya


def op_rename_attribute(node, long_name, new_long_name, new_nice_name=""):
    attr_value = Maya.get_attribute(node, long_name)
    if not attr_value:
        attr_value = ""
    op_del_attribute(node, long_name)
    op_add_attribute(
        node=node,
        long_name=new_long_name,
        nice_name=new_nice_name,
        default_value=attr_value,
    )


def op_add_attribute(node, long_name, nice_name="", default_value=""):
    Maya.add_attribute(
        node=node,
        long_name=long_name,
        nice_name=nice_name,
        default_value=default_value,
    )


def op_set_attribute(node, attr, attr_value):
    Maya.set_attribute(node, attr, attr_value)


def op_del_attribute(node, attr):
    Maya.del_attribute(node, attr)
    Maya.select(node)
