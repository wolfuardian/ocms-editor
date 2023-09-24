import ocmseditor.oe.qt as qt
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

        self.groupbox_manager = qt.QtGroupboxManager()

        self.attr_tool_box = qt.QtGroupVBoxCSWidget()
        self.attr_tool_box.set_text("屬性工具")

        self.add_comp_attr_to_sel_single_obj_btn = qt.QtButtonCSWidget()
        self.add_comp_attr_to_sel_single_obj_btn.set_text("新增  選取的  單個物體  複合屬性")

        self.add_attr_to_sel_single_obj_btn = qt.QtButtonCSWidget()
        self.add_attr_to_sel_single_obj_btn.set_text("新增  選取的  單個物體  屬性")

        self.add_comp_attr_to_sel_single_obj_btn.clicked.connect(
            lambda: operator.op_add_comp_attr_to_sel_single_obj(self)
        )
        self.add_attr_to_sel_single_obj_btn.clicked.connect(
            lambda: operator.op_add_attr_to_sel_single_obj(self)
        )

        self.attr_tool_box.layout.addWidget(self.add_comp_attr_to_sel_single_obj_btn)
        self.attr_tool_box.layout.addWidget(self.add_attr_to_sel_single_obj_btn)

        self.scrollarea.layout.addWidget(self.attr_tool_box)
        self.scrollarea.layout.addWidget(self.groupbox_manager.get_groupbox())

        self.frame_layout.addWidget(self.scrollarea)

        self._validate()
        self._construct_met_edit_panel()

        operator.subscribe_event()

    def redraw_met_edit_panel(self):
        self._destroy_met_edit_panel()
        self._construct_met_edit_panel()

    def _destroy_met_edit_panel(self):
        self.groupbox_manager.clear_all()

    def _preconstruct(self, project_dir):
        pass
        # tool.Widget.set_text(self.project_dir_txt.lineedit, project_dir)

    def _validate(self):
        helper.Logger.info(__name__, "Validating...")
        # Operator: Validate
        # project_path = tool.Registry.get_reg(const.REG_PROJ_PATH)
        self._preconstruct(...)

    def _construct_met_edit_panel(self):
        self.groupbox_manager.add_group(
            widget_id="點位物件統計", widget=qt.QtGroupVBoxCSWidget(text="點位物件統計")
        )
