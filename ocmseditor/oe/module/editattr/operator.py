import ocmseditor.oe.qt as qt
import ocmseditor.tool as tool
import ocmseditor.oe.handler as handler

import ocmseditor.oe.helper as helper

from .data import TreeItemsData, MayaNodesData


def op_serialized_tree_data(self):
    ocms = tool.OCMS.get_ocms()

    ocms.met.update_data()

    TreeItemsData.update(self.tree)
    TreeItemsData.expand_all(True)

    MayaNodesData.update()


def op_add_element(self):
    ocms = tool.OCMS.get_ocms()
    parent_uuid = self.tree.currentItem().text(0)
    parent_type = parent_uuid.split("-")[1]

    if parent_type == "Device":
        helper.Logger.warning(__name__, "Cannot add Device under Device!")
        return

    _available_index = 1
    for uuid, data in ocms.met.get_data().items():
        if data["global"]["index"] == _available_index:
            _available_index += 1
            continue
        else:
            break
    process_index = tool.UUID.format_number_with_digits(_available_index, 4)
    uuid = tool.UUID.generate_ocms_uuid(
        type_str="Device",
        model="",
        number=process_index,
    )
    ocms.met.add_element(uuid, parent_uuid)
    TreeItemsData.add_tree_element(uuid, parent_uuid)
    MayaNodesData.add_maya_group(uuid, parent_uuid)


def op_del_element(self):
    ocms = tool.OCMS.get_ocms()
    uuid = self.tree.currentItem().text(0)
    parent_uuid = ocms.met.get_data()[uuid]["maya"]["parent"]
    TreeItemsData.del_tree_element(uuid, parent_uuid)
    MayaNodesData.del_maya_group(uuid, parent_uuid)
    ocms.met.del_element(uuid, parent_uuid)


def op_expand_all(self):
    TreeItemsData.expand_all(True)


def op_add_comp_attr_to_sel_single_obj(self):
    sel_obj = tool.Maya.get_selected()[0]


def op_add_attr_to_sel_single_obj(self):
    sel_obj = tool.Maya.get_selected()[0]


def subscribe_event(self):
    handler.EventHub.subscribe(
        "on_maya_selection_changed", lambda: on_maya_selection_changed(self)
    )
    handler.EventHub.subscribe("on_maya_selection_changed", on_maya_update_met_panel)


def on_maya_selection_changed(self):
    ocms = tool.OCMS.get_ocms()
    maya = ocms.maya
    if len(tool.Maya.get_selected()) == 0:
        return
    maya.active_object = tool.Maya.get_selected()[0]
    self.select_obj_name_txt.set_text(maya.active_object)


def on_maya_update_met_panel():
    ocms = tool.OCMS.get_ocms()
    __ui = ocms.ui.context.get("frame_edit_attr")
    if __ui:
        __ui.redraw_met_edit_panel()


def op_treeitem_selection_changed(self):
    ocms = tool.OCMS.get_ocms()
    _cur_active_obj = ocms.maya.active_object
    ocms.maya.active_object = self.tree.currentItem().text(0)
    maya_active_obj = tool.Name.to_underscore(ocms.maya.active_object)
    if tool.Maya.obj_exists(maya_active_obj):
        tool.Maya.select(maya_active_obj)
    else:
        ocms.maya.active_object = _cur_active_obj
        helper.Logger.warning(__name__, "Object does not exist in Maya scene!")
