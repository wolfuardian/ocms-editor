from functools import partial
from ocmseditor.oe.utils.qt import (
    QtCore,
    QtWidgets,
    QtFloatCSWidget,
    QtScrollareaCSWidget,
    QtFramelessLayoutCSWidget,
    QtGroupVBoxCSWidget,
    QtGroupVContainerCSWidget,
    QtGroupHBoxCSWidget,
    QtGroupHBoxCSWidget,
    QtHeadingLabelCSWidget,
    QtButtonCSWidget,
    QtStringPropertyCSWidget,
    get_main_window,
)
from ocmseditor.oe.utils.qt_stylesheet import (
    QtGroupBoxStyle,
    QtButtonStyle,
    QtTitleLabelStyle,
    QtPropertyStyle,
)
from ocmseditor.oe.constant import AttributePanel, AttributeType
from ocmseditor.oe.repository import RepositoryFacade
from .operator import op_set_attr_name, op_set_attr_prop, op_del_attr
from ocmseditor.tool.maya import Maya

global instance_edit_attribute


class EditAttributeWidget(QtFramelessLayoutCSWidget):
    def __init__(self):
        super().__init__()
        self.panel_status = AttributePanel.Expanded

        self.__container_v_box = QtGroupVBoxCSWidget()
        self.__container_v_box.layout.setContentsMargins(0, 0, 0, 0)
        self.__container_v_box.layout.setSpacing(0)

        self.__container_h_box = QtGroupHBoxCSWidget()
        self.__container_h_box.layout.setContentsMargins(0, 0, 0, 0)
        self.__container_h_box.layout.setSpacing(0)
        self.__container_h_box.setFixedWidth(300)
        self.__container_h_box.setFixedHeight(600)

        self.__container_h_box.set_resizeable(True)
        self.__container_h_box.sizeSetter.connect(
            lambda size: self.__container_h_box.setFixedSize(size)
        )
        self.__container_h_box.set_edge_distance(4)
        self.__container_h_box.setStyleSheet(QtGroupBoxStyle.Transparent)
        self.__container_h_box_org_stylesheet = self.__container_h_box.styleSheet()
        self.__container_h_box_new_stylesheet = """\nQGroupBox {
                border-right: 4px solid #363636;
                border-bottom: 4px solid #363636;
            }"""
        self.__container_h_box.setStyleSheet(
            self.__container_h_box_org_stylesheet
            + self.__container_h_box_new_stylesheet
        )

        self.__container_collapse_btn = QtButtonCSWidget()
        self.__container_collapse_btn.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
        )
        self.__container_collapse_btn.setFixedWidth(8)
        self.__container_collapse_btn.set_icon(":/nodeGrapherPrevious.png")
        self.__container_collapse_btn.setStyleSheet(QtButtonStyle.Dark)

        self.__scrollarea = QtScrollareaCSWidget()
        self.__scrollarea.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding
        )
        self.__scrollarea.setAlignment(QtCore.Qt.AlignTop)

        self.__attributes_v_box = QtGroupVBoxCSWidget()
        self.__attributes_v_box.layout.setContentsMargins(0, 0, 0, 0)
        self.__attributes_v_box.layout.setSpacing(0)
        self.__attributes_v_box.setStyleSheet(QtGroupBoxStyle.Transparent)

        self.__attributes_props_v_container = QtGroupVContainerCSWidget()
        self.__attributes_props_v_container.layout.setContentsMargins(3, 3, 3, 3)
        self.__attributes_props_v_container.layout.setSpacing(12)

        self.__inspector_title_h_box = QtGroupHBoxCSWidget()
        self.__inspector_title_h_box.layout.setContentsMargins(0, 0, 0, 0)
        self.__inspector_title_h_box.setStyleSheet(QtGroupBoxStyle.White)

        self.__inspector_title = QtHeadingLabelCSWidget()
        self.__inspector_title.setText("Inspector")
        self.__inspector_title.set_heading(5)
        self.__inspector_title.setStyleSheet(QtTitleLabelStyle.Black)

        self.__imports_btn_h_box = QtGroupHBoxCSWidget()

        self.__imports_btn_h_box.layout.setContentsMargins(0, 0, 0, 0)
        self.__imports_btn_h_box.layout.setSpacing(0)
        self.__imports_btn_h_box.setStyleSheet(QtGroupBoxStyle.Transparent)

        self.__title_h = QtHeadingLabelCSWidget()
        self.__title_h.setText("Import From")
        self.__title_h.set_heading(5)

        self.edit_attribute = self.__create_edit_attribute()

        self.__container_collapse_btn.clicked.connect(self.toggle_panel)

        self.__inspector_title_h_box.layout.addWidget(self.__inspector_title)
        self.__attributes_v_box.layout.addWidget(self.__inspector_title_h_box)
        self.__attributes_v_box.layout.addWidget(self.__attributes_props_v_container)

        self.__scrollarea.layout.addWidget(self.__attributes_v_box)

        self.__container_v_box.layout.addWidget(self.__scrollarea)

        self.__container_h_box.layout.addWidget(self.__container_v_box)
        self.__container_h_box.layout.addWidget(self.__container_collapse_btn)
        self.__container_h_box.layout.addWidget(self.__container_collapse_btn)

        self.edit_attribute.layout.addWidget(self.__container_h_box)

        self.__add_ac_object_btn = None
        self.__add_ac_component_legacy_btn = None
        self.__add_ac_component_btn = None

    def toggle_panel(self):
        if self.panel_status == AttributePanel.Expanded:
            self.__container_collapse_btn.set_icon(":/nodeGrapherNext.png")
            self.__container_v_box.setVisible(False)
            self.panel_status = AttributePanel.Collapsed
            self.__container_h_box.setStyleSheet(self.__container_h_box_org_stylesheet)
        elif self.panel_status == AttributePanel.Collapsed:
            self.__container_collapse_btn.set_icon(":/nodeGrapherPrevious.png")
            self.__container_v_box.setVisible(True)
            self.panel_status = AttributePanel.Expanded
            self.__container_h_box.setStyleSheet(
                self.__container_h_box_org_stylesheet
                + self.__container_h_box_new_stylesheet
            )

    def redraw_edit_attributes(self):
        self.destroy_edit_attributes()
        self.construct_edit_attributes()

    def destroy_edit_attributes(self):
        self.__attributes_props_v_container.clear_all()

    def construct_edit_attributes(self):
        maya = RepositoryFacade().maya

        attrs = Maya.get_attrs(maya.selected_object)
        parsing_attrs = Maya.parse_attrs(attrs)
        for attr_typ, attr_data in parsing_attrs.items():
            for compound, props in attr_data.items():
                for prop, value in props.items():
                    print(f"attr_typ, compound, prop, value = {attr_typ}, {compound}, {prop}, {value}")
        return
        


















        for attr, attr_value in Maya.get_attrs(maya.selected_object).items():
            attr_type = Maya.parse_attribute_type(attr)
            compound = ""
            attr_str = ""
            if attr_type == AttributeType.Object:
                compound = attr.split("_")[0]
            elif attr_type == AttributeType.ComponentV2:
                compound = ".".join(attr.split("_")[1:-1])
            elif attr_type == AttributeType.Component:
                compound = ".".join(attr.split("_")[1:-1])
            else:
                compound = "Undefined"
                print(f"Something wrong with attr: {attr}")
            __group = QtGroupVBoxCSWidget(title=compound)
            __group.setStyleSheet(QtGroupBoxStyle.Minimal)
            print(f"compound_attrs = {compound}")
            if not self.__attributes_props_v_container.is_group_exist(compound):
                self.__attributes_props_v_container.add_group(
                    group_id=compound, widget=__group
                )
            __prop_lineedit = QtStringPropertyCSWidget(
                attr=attr,
                attr_str=attr_str,
                attr_value=attr_value,
            )
            __prop_lineedit.setStyleSheet(QtPropertyStyle.Minimal)
            self.__attributes_props_v_container.add_widget(
                group_id=compound, widget_id=attr, widget=__prop_lineedit
            )
            if not self.__attributes_props_v_container.is_group_exist(compound):
                __add_attr_btn = QtButtonCSWidget()
                __add_attr_btn.setFixedHeight(10)
                __add_attr_btn.set_icon("plus-8px.png")
                __add_attr_btn.setStyleSheet(QtButtonStyle.Default_Roundness)
                maya = RepositoryFacade().maya
                __add_attr_btn.clicked.connect(partial(self.add_attr, compound))
                self.__attributes_props_v_container.add_widget(
                    group_id=compound,
                    widget_id=compound + "_" + "add_attr_btn",
                    widget=__add_attr_btn,
                )
        # return
        # for compound_attr, attrs in attrs.items():
        #     print(f"compound_attr, attrs = {compound_attr}, {attrs}")
        #     __group = QtGroupVBoxCSWidget(title=compound_attr.capitalize())
        #     __group.setStyleSheet(QtGroupBoxStyle.Minimal)
        #
        #     self.__attributes_props_v_container.add_group(
        #         group_id=compound_attr, widget=__group
        #     )
        #     for attr, attr_value in attrs.items():
        #         __prop_lineedit = QtStringPropertyCSWidget(
        #             attr_long=attr,
        #             compound=compound_attr,
        #             attr=attr,
        #             value=attr_value,
        #         )
        #         __prop_lineedit.setStyleSheet(QtPropertyStyle.Minimal)
        #         self.__attributes_props_v_container.add_widget(
        #             group_id=compound_attr, widget_id=attr, widget=__prop_lineedit
        #         )
        #         __prop_lineedit.lineedit.setCursorPosition(0)
        #         __prop_lineedit.attrSetter.connect(self.set_attr_name)
        #         __prop_lineedit.attrPropSetter.connect(self.set_attr_value)
        #         __prop_lineedit.attrDeleter.connect(self.del_attr)


        __tool_gp = QtGroupHBoxCSWidget()
        __tool_gp.layout.setContentsMargins(0, 0, 0, 0)
        __tool_gp.layout.setSpacing(3)
        __tool_gp.setStyleSheet(QtGroupBoxStyle.Transparent)
        # __tool_gp.setFixedHeight(32)
        # __tool_gp.setFixedWidth(96)
        # __tool_gp.set_icon("plus.png")
        # __tool_gp.setText("新增屬性集")
        # __tool_gp.setStyleSheet(QtButtonStyle.Default_Roundness)
        # __tool_gp.clicked.connect(self.add_compound_attr)
        self.__attributes_props_v_container.add_group(
            group_id="tool_gp", widget=__tool_gp
        )
        self.__add_ac_object_btn = QtButtonCSWidget()
        self.__add_ac_object_btn.setFixedHeight(32)
        self.__add_ac_object_btn.setFixedWidth(96)
        self.__add_ac_object_btn.set_icon("plus.png")
        self.__add_ac_object_btn.setText("  新增 Object")
        self.__add_ac_object_btn.setStyleSheet(QtButtonStyle.Default_Roundness)
        self.__add_ac_object_btn.clicked.connect(self.add_ac_object)
        self.__attributes_props_v_container.add_widget(
            group_id="tool_gp",
            widget_id="add_compound_attr_btn",
            widget=self.__add_ac_object_btn,
        )
        self.__add_ac_component_legacy_btn = QtButtonCSWidget()
        self.__add_ac_component_legacy_btn.setFixedHeight(32)
        self.__add_ac_component_legacy_btn.setFixedWidth(128)
        self.__add_ac_component_legacy_btn.set_icon("add_component_legacy.png")
        self.__add_ac_component_legacy_btn.setText("  新增 Component")
        self.__add_ac_component_legacy_btn.setStyleSheet(
            QtButtonStyle.Default_Roundness
        )
        self.__add_ac_component_legacy_btn.clicked.connect(self.add_ac_component_legacy)
        self.__attributes_props_v_container.add_widget(
            group_id="tool_gp",
            widget_id="add_ac_component_legacy_btn",
            widget=self.__add_ac_component_legacy_btn,
        )
        self.__add_ac_component_btn = QtButtonCSWidget()
        self.__add_ac_component_btn.setFixedHeight(32)
        self.__add_ac_component_btn.setFixedWidth(128)
        self.__add_ac_component_btn.set_icon("add_component.png")
        self.__add_ac_component_btn.setText("  新增 Component")
        self.__add_ac_component_btn.setStyleSheet(QtButtonStyle.Default_Roundness)
        self.__add_ac_component_btn.clicked.connect(self.add_ac_component)
        self.__attributes_props_v_container.add_widget(
            group_id="tool_gp",
            widget_id="add_ac_component_btn",
            widget=self.__add_ac_component_btn,
        )
        # 對欄位操作的按鈕
        self.__validate_attrs()

    def __validate_attrs(self):
        # Object_type
        # Object_category
        # Object_name
        # Object_alias
        # Object_remark
        # Object_time
        # Object_noted

        # len = 2

        # Component_OCMS_Scene_FocusAt_pitch
        # Component_OCMS_Scene_FocusAt_yaw
        # Component_OCMS_Scene_FocusAt_zoom
        # Component_OCMS_Scene_FocusAt_offset

        # Component_NADILeanTouch_LeanCameraSettingValue_zoom
        # Component_NADILeanTouch_LeanCameraSettingValue_pitchWawSensitivity
        # Component_NADILeanTouch_LeanCameraSettingValue_pitchYaw
        # Component_NADILeanTouch_LeanCameraSettingValue_offset
        # len >= 3

        maya = RepositoryFacade().maya
        attrs = Maya.get_attrs(maya.selected_object)
        for attr, attr_value in attrs.items():
            print(f"attr, attr_value = {attr}, {attr_value}")

        if self.__has_ac_object():
            self.__add_ac_object_btn.setVisible(False)

        if self.__has_ac_component_legacy():
            self.__add_ac_component_legacy_btn.setVisible(False)

        if self.__has_ac_component():
            self.__add_ac_component_btn.setVisible(False)

    @staticmethod
    def __has_ac_object():
        maya = RepositoryFacade().maya
        compound_attrs = Maya.get_attrs_hierarchy(maya.selected_object)
        return "Object" in compound_attrs.keys()

    @staticmethod
    def __has_ac_component_legacy():
        maya = RepositoryFacade().maya
        compound_attrs = Maya.get_attrs_hierarchy(maya.selected_object)
        component_attrs = [c for c in compound_attrs.keys() if "ComponentV2" in c]
        return len(component_attrs) > 0

    @staticmethod
    def __has_ac_component():
        maya = RepositoryFacade().maya
        compound_attrs = Maya.get_attrs_hierarchy(maya.selected_object)
        component_attrs = [
            c for c in compound_attrs.keys() if "Component" in c and c != "ComponentV2"
        ]
        return len(component_attrs) > 0

    @staticmethod
    def set_attr_name(compound, old_attr, new_attr):
        maya = RepositoryFacade().maya
        maya.selected_attribute = compound + "_" + old_attr
        new_attr = compound + "_" + new_attr
        op_set_attr_name(maya.selected_object, maya.selected_attribute, new_attr)

    @staticmethod
    def set_attr_value(compound, attr, value):
        maya = RepositoryFacade().maya
        maya.selected_attribute = compound + "_" + attr
        op_set_attr_prop(maya.selected_object, maya.selected_attribute, value)

    @staticmethod
    def del_attr(compound, attr):
        maya = RepositoryFacade().maya
        maya.selected_attribute = compound + "_" + attr
        op_del_attr(maya.selected_object, maya.selected_attribute)

    @staticmethod
    def add_attr(compound):
        maya = RepositoryFacade().maya
        input_attr = Maya.user_input_dialog(message="屬性名稱 attr 為:")
        if input_attr:
            Maya.add_attr(maya.selected_object, compound, input_attr)
            Maya.select(maya.selected_object)
        input_value = Maya.user_input_dialog(message="屬性值 value 為:")
        if input_value:
            maya = RepositoryFacade().maya
            maya.selected_attribute = compound + "_" + input_attr
            op_set_attr_prop(maya.selected_object, maya.selected_attribute, input_value)

    @staticmethod
    def add_ac_object():
        maya = RepositoryFacade().maya
        Maya.new_attribute(maya.selected_object, AttributeType.Object)
        Maya.select(maya.selected_object)

    @staticmethod
    def add_ac_component_legacy():
        maya = RepositoryFacade().maya
        Maya.new_attribute(maya.selected_object, AttributeType.ComponentV2)
        Maya.select(maya.selected_object)

    @staticmethod
    def add_ac_component():
        maya = RepositoryFacade().maya
        Maya.new_attribute(maya.selected_object, AttributeType.Component)
        Maya.select(maya.selected_object)

    @staticmethod
    def __create_edit_attribute():
        global instance_edit_attribute
        parent = get_main_window()
        try:
            if instance_edit_attribute:
                instance_edit_attribute.close()
                instance_edit_attribute.deleteLater()
                instance_edit_attribute = QtFloatCSWidget(parent=parent)
                instance_edit_attribute.update()
                instance_edit_attribute.show()

        except NameError:
            instance_edit_attribute = QtFloatCSWidget(parent=parent)
            instance_edit_attribute.update()
            instance_edit_attribute.show()

        except RuntimeError:
            instance_edit_attribute = QtFloatCSWidget(parent=parent)
            instance_edit_attribute.update()
            instance_edit_attribute.show()
        return instance_edit_attribute
