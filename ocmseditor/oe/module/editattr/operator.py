import ocmseditor.tool as tool
import ocmseditor.oe.handler as handler


def op_add_comp_attr_to_sel_single_obj(self):
    sel_obj = tool.Maya.get_selected()[0]
    # tool.Maya.add_compound_attr(sel_obj, "test", 3)


def op_add_attr_to_sel_single_obj(self):
    sel_obj = tool.Maya.get_selected()[0]
    # tool.Maya.add_string_attr(sel_obj, "test123", "test", "test")


def subscribe_event():
    handler.EventHub.subscribe("on_maya_selection_changed", on_maya_selection_changed)
    handler.EventHub.subscribe("on_maya_selection_changed", on_maya_update_met_panel)


def on_maya_selection_changed():
    ocms = tool.OCMS.get_ocms()
    maya = ocms.maya
    maya.active_object = tool.Maya.get_selected()[0]


def on_maya_update_met_panel():
    ocms = tool.OCMS.get_ocms()
    __ui = ocms.ui.context.get("frame_edit_attr")
    if __ui:
        __ui.redraw_met_edit_panel()

