import ocmseditor.oe.qt as qt
import ocmseditor.tool as tool
import ocmseditor.oe.helper as helper

from . import operator


class EditAttributeCSWidget(qt.QtFrameLayoutCSWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.set_text("編輯 Maya 屬性")

        self.scrollarea = qt.QtScrollareaCSWidget()
        self.scrollarea.setSizePolicy(
            qt.QtWidgets.QSizePolicy.Expanding, qt.QtWidgets.QSizePolicy.Expanding
        )

        # self.groupbox_manager = qt.QtGroupboxManager()

        self.attr_tool_box = qt.QtGroupVBoxCSWidget()
        self.attr_tool_box.set_text("屬性工具")

        self.attr_prop_box = qt.QtGroupVBoxCSWidget()
        self.attr_prop_box.set_text("屬性編輯器")
        # self.attr_prop_box.layout.setContentsMargins(0, 0, 0, 0)
        self.attr_prop_box.layout.setSpacing(0)

        self.attr_prop_scrollarea = qt.QtScrollareaCSWidget()
        self.attr_prop_scrollarea.setSizePolicy(
            qt.QtWidgets.QSizePolicy.Expanding, qt.QtWidgets.QSizePolicy.Expanding
        )

        self.serialized_btn = qt.QtButtonCSWidget()
        self.serialized_btn.set_icon(":/RS_accept_import.png")
        self.serialized_btn.set_text("串接OCMS資料")
        self.serialized_btn.set_status(qt.QtButtonStatus.Disable)
        # self.fetch_btn.set_width(4)
        self.serialized_btn.set_height(20)
        self.serialized_btn.set_tooltip("Fetch")

        self.select_obj_name_txt = qt.QtTextLineCSWidget()
        self.select_obj_name_txt.set_title("選擇的物件")
        self.select_obj_name_txt.set_text("")

        self.tree_box = qt.QtGroupHBoxCSWidget()
        self.tree_box.layout.setAlignment(qt.QtCore.Qt.AlignTop)
        self.tree_box.layout.setContentsMargins(0, 0, 0, 0)
        self.tree_box.layout.setSpacing(0)
        self.tree_box.set_status(qt.QtGroupBoxStatus.Transparent)

        self.tree_tool_box = qt.QtGroupVBoxCSWidget()
        self.tree_tool_box.layout.setAlignment(qt.QtCore.Qt.AlignTop)
        self.tree_tool_box.layout.setContentsMargins(0, 0, 3, 0)
        self.tree_tool_box.layout.setSpacing(3)
        self.tree_tool_box.set_status(qt.QtGroupBoxStatus.Transparent)

        self.add_node_btn = qt.QtButtonCSWidget()
        self.add_node_btn.set_icon(":/nodeGrapherAddNodes.png")
        self.add_node_btn.set_width(20)
        self.add_node_btn.set_height(20)
        self.add_node_btn.set_status(qt.QtButtonStatus.Transparent)

        self.remove_node_btn = qt.QtButtonCSWidget()
        self.remove_node_btn.set_icon(":/nodeGrapherRemoveNodes.png")
        self.remove_node_btn.set_width(20)
        self.remove_node_btn.set_height(20)
        self.remove_node_btn.set_status(qt.QtButtonStatus.Transparent)

        self.expand_all_btn = qt.QtButtonCSWidget()
        self.expand_all_btn.set_icon(":/nodeGrapherUpDown.png")
        self.expand_all_btn.set_width(20)
        self.expand_all_btn.set_height(20)
        self.expand_all_btn.set_status(qt.QtButtonStatus.Transparent)

        self.tree = qt.QtTreeCSWidget()
        self.tree.setHeaderLabels(["Hierarchy"])
        self.tree.setCurrentItem(self.tree.topLevelItem(0))

        self.attr_prop_container = qt.QtGroupboxManager()

        self.tree.set_selection_changed_event(
            lambda: operator.op_treeitem_selection_changed(self)
        )
        self.serialized_btn.clicked.connect(
            lambda: operator.op_serialized_tree_data(self)
        )
        self.add_node_btn.clicked.connect(lambda: operator.op_add_element(self))
        self.remove_node_btn.clicked.connect(lambda: operator.op_del_element(self))
        self.expand_all_btn.clicked.connect(lambda: operator.op_expand_all(self))

        self.attr_tool_box.layout.addWidget(self.serialized_btn)
        self.attr_tool_box.layout.addWidget(self.select_obj_name_txt)

        self.tree_tool_box.layout.addWidget(self.add_node_btn)
        self.tree_tool_box.layout.addWidget(self.remove_node_btn)
        self.tree_tool_box.layout.addWidget(self.expand_all_btn)

        self.tree_box.layout.addWidget(self.tree_tool_box)
        self.tree_box.layout.addWidget(self.tree)

        self.attr_tool_box.layout.addWidget(self.tree_box)

        self.attr_prop_box.layout.addWidget(self.attr_prop_container.get_groupbox())
        self.attr_prop_scrollarea.layout.addWidget(self.attr_prop_box)

        self.scrollarea.layout.addWidget(self.attr_tool_box)
        self.scrollarea.layout.addWidget(self.attr_prop_scrollarea)

        self.frame_layout.addWidget(self.scrollarea)

        self._validate()
        # self._construct_met_edit_panel()

        operator.subscribe_event(self)

    def _preconstruct(self, project_dir):
        pass
        # tool.Widget.set_text(self.project_dir_txt.lineedit, project_dir)

    def _validate(self):
        helper.Logger.info(__name__, "Validating...")
        # Operator: Validate
        # project_path = tool.Registry.get_reg(const.REG_PROJ_PATH)
        self._preconstruct(...)

    def redraw_met_edit_panel(self, context):
        self._destroy_met_edit_panel(context)
        self._construct_met_edit_panel(context)

    def _destroy_met_edit_panel(self, context):
        self.attr_prop_container.clear_all()

    def prop_setter(self, long_name, nice_name, value):
        ocms = tool.OCMS.get_ocms()
        obj_name = ocms.maya.active_object
        operator.op_set_attr(obj_name, long_name, value)

    def _construct_met_edit_panel(self, context):
        for attr_name, attr_value in context["attrs"].items():
            if isinstance(attr_value, str):
                continue
            elif isinstance(attr_value, dict):
                compound_name = attr_name
                self.attr_prop_container.add_group(
                    widget_id=compound_name,
                    widget=qt.QtGroupVBoxCSWidget(text=compound_name),
                )
                for _attr_nm, _attr_val in attr_value.items():
                    _prop = qt.QtStringPropertyCSWidget(
                        long_name=compound_name + "." + _attr_nm,
                        nice_name=_attr_nm.capitalize(),
                        value=_attr_val,
                    )
                    self.attr_prop_container.add_widget(
                        parent_id=compound_name,
                        widget_id=_attr_nm,
                        widget=_prop,
                    )
                    _prop.lineedit.setCursorPosition(0)
                    _prop.propertySetter.connect(self.prop_setter)
