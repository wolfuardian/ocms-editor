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
from ocmseditor.oe.constant import AttributePanel, Attribute, AttributeType
from ocmseditor.oe.repository import RepositoryFacade
from .operator import (
    op_add_attribute,
    op_del_attribute,
    op_set_attribute,
    op_rename_attribute,
)
from ocmseditor.tool.maya import Maya
from ocmseditor.tool.debug import Debug

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

        self.__attributes_v_container = QtGroupVContainerCSWidget()
        self.__attributes_v_container.layout.setContentsMargins(3, 3, 3, 3)
        self.__attributes_v_container.layout.setSpacing(12)

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
        self.__attributes_v_box.layout.addWidget(self.__attributes_v_container)

        self.__scrollarea.layout.addWidget(self.__attributes_v_box)

        self.__container_v_box.layout.addWidget(self.__scrollarea)

        self.__container_h_box.layout.addWidget(self.__container_v_box)
        self.__container_h_box.layout.addWidget(self.__container_collapse_btn)
        self.__container_h_box.layout.addWidget(self.__container_collapse_btn)

        self.edit_attribute.layout.addWidget(self.__container_h_box)

        self.__add_object_compound_btn = None
        self.__add_component_compound_btn = None

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
        self.__attributes_v_container.clear_all()

    def construct_edit_attributes(self):
        maya = RepositoryFacade().maya
        ui = RepositoryFacade().ui
        print(
            "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        )
        ui.attributes = Maya.get_attributes(maya.selected_object)
        print("attributes:")
        Debug.print_beautiful_dictionary(ui.attributes, 0, "    ")
        print("\n")
        ui.attributes_data = Maya.parse_attributes(ui.attributes)

        print("attributes_data:")
        Debug.print_beautiful_dictionary(ui.attributes_data, 0, "    ")
        print("\n")

        print("redirected_attributes_data:")
        ui.redirected_attributes_data = Maya.sort_parsed_attributes(ui.attributes_data)
        Debug.print_beautiful_dictionary(ui.redirected_attributes_data, 0, "    ")
        print("\n")

        for attr_typ, attr_data in ui.redirected_attributes_data.items():
            for compound, props in attr_data.items():
                __is_compound_error = False
                __compound_v_box = QtGroupVBoxCSWidget(title=compound)
                if attr_typ == AttributeType.Undefined:
                    __compound_v_box.setStyleSheet(QtGroupBoxStyle.Minimal_Error)
                    __is_compound_error = True
                else:
                    __compound_v_box.setStyleSheet(QtGroupBoxStyle.Minimal)
                    __is_compound_error = False
                self.__attributes_v_container.add_group(
                    group_id=compound, widget=__compound_v_box
                )
                for prop, pdata in props.items():
                    pdata: dict
                    long_name = pdata.get(Attribute.LongName)
                    short_name = pdata.get(Attribute.ShortName)
                    nice_name = pdata.get(Attribute.NiceName)
                    string_property = pdata.get(Attribute.StringProperty)
                    __string_property = QtStringPropertyCSWidget(
                        long_name=long_name,
                        short_name=short_name,
                        nice_name=nice_name,
                        string_property=string_property,
                    )
                    __string_property.setStyleSheet(QtPropertyStyle.Minimal)
                    self.__attributes_v_container.add_widget(
                        group_id=compound,
                        widget_id=long_name + "__string_property",
                        widget=__string_property,
                    )
                    __string_property.attributeValidator.connect(
                        partial(self.validate_attribute, __string_property)
                    )
                    __string_property.attributeRenamer.connect(self.rename_attribute)
                    __string_property.attributeSetter.connect(self.set_attribute)
                    __string_property.attributeDeleter.connect(self.del_attribute)

                if __is_compound_error:
                    continue
                __add_attr_btn = QtButtonCSWidget()
                __add_attr_btn.setFixedHeight(10)
                __add_attr_btn.set_icon("plus-8px.png")
                __add_attr_btn.setStyleSheet(QtButtonStyle.Default_Roundness)
                __add_attr_btn.clicked.connect(
                    partial(self.add_attribute_to_exist_compound, attr_typ, compound)
                )
                self.__attributes_v_container.add_widget(
                    group_id=compound,
                    widget_id=compound + "__add_attr_btn",
                    widget=__add_attr_btn,
                )

        __toolbox_h_box = QtGroupHBoxCSWidget()
        __toolbox_h_box.layout.setContentsMargins(0, 0, 0, 0)
        __toolbox_h_box.layout.setSpacing(3)
        __toolbox_h_box.setStyleSheet(QtGroupBoxStyle.Transparent)

        self.__attributes_v_container.add_group(
            group_id="__toolbox_h_box", widget=__toolbox_h_box
        )
        self.__add_object_compound_btn = QtButtonCSWidget()
        self.__add_object_compound_btn.setFixedHeight(32)
        self.__add_object_compound_btn.setFixedWidth(96)
        self.__add_object_compound_btn.set_icon("plus.png")
        self.__add_object_compound_btn.setText("  新增 Object")
        self.__add_object_compound_btn.setStyleSheet(QtButtonStyle.Default_Roundness)
        self.__add_object_compound_btn.clicked.connect(self.add_ac_object)
        self.__attributes_v_container.add_widget(
            group_id="__toolbox_h_box",
            widget_id="__add_object_compound_btn",
            widget=self.__add_object_compound_btn,
        )
        self.__add_component_compound_btn = QtButtonCSWidget()
        self.__add_component_compound_btn.setFixedHeight(32)
        self.__add_component_compound_btn.setFixedWidth(128)
        self.__add_component_compound_btn.set_icon("add_component.png")
        self.__add_component_compound_btn.setText("  新增 Component")
        self.__add_component_compound_btn.setStyleSheet(QtButtonStyle.Default_Roundness)
        self.__add_component_compound_btn.clicked.connect(self.add_ac_component)
        self.__attributes_v_container.add_widget(
            group_id="__toolbox_h_box",
            widget_id="__add_component_compound_btn",
            widget=self.__add_component_compound_btn,
        )

        self.__hide_button_when_object_compound_exist()

    def __hide_button_when_object_compound_exist(self):
        if self.__has_object_compound():
            self.__add_object_compound_btn.setVisible(False)
        else:
            self.__add_component_compound_btn.setVisible(False)

    @staticmethod
    def __has_object_compound():
        ui = RepositoryFacade().ui
        return AttributeType.Object in ui.redirected_attributes_data.keys()

    @staticmethod
    def validate_attribute(this_widget, original_name, current_name):
        def __is_valid(s):
            import re

            return bool(re.fullmatch(r"[a-zA-Z0-9]*_?[a-zA-Z0-9]*", s))

        def __invalid_edit():
            print("錯誤: 輸入字符中有英、數、底線以外的字元。")
            return original_name

        def __pass_edit():
            return "pass"

        def __valid_edit():
            return current_name

        if not __is_valid(current_name):
            __attr = __invalid_edit()
            this_widget.editable_label.setText(__attr)
        elif current_name == original_name:
            __attr = __pass_edit()
            pass
        else:
            __attr = __valid_edit()
            this_widget.editable_label.editApply.emit(original_name, current_name)

    @staticmethod
    def rename_attribute(long_name, nice_name, old_short_name, new_short_name):
        maya = RepositoryFacade().maya
        maya.selected_attribute = long_name
        new_long_name = long_name.replace(old_short_name, new_short_name)
        new_nice_name = nice_name.replace(old_short_name, new_short_name)
        op_rename_attribute(
            node=maya.selected_object,
            long_name=maya.selected_attribute,
            new_long_name=new_long_name,
            new_nice_name=new_nice_name,
        )
        Maya.select(maya.selected_object)

    @staticmethod
    def set_attribute(long_name, value):
        maya = RepositoryFacade().maya
        maya.selected_attribute = long_name
        op_set_attribute(maya.selected_object, maya.selected_attribute, value)

    @staticmethod
    def del_attribute(long_name):
        maya = RepositoryFacade().maya
        maya.selected_attribute = long_name
        op_del_attribute(maya.selected_object, maya.selected_attribute)

    @staticmethod
    def add_attribute_to_exist_compound(attr_typ, compound):
        maya = RepositoryFacade().maya
        _input = Maya.input_dialog(message="屬性名稱 attr 為:")
        if not _input:
            _input = "default"
        if attr_typ == AttributeType.Object:
            long_name = AttributeType.Object + "_" + _input
        elif attr_typ == AttributeType.Component:
            long_name = (
                AttributeType.Component
                + "_"
                + compound.replace(".", "_")
                + "_"
                + _input
            )
        else:
            raise Exception("Undefined Attribute Type")
        if Maya.has_attribute(maya.selected_object, long_name):
            print("錯誤: 該屬性已經存在。")
            return

        _input = Maya.input_dialog(message="屬性值 value 為:")
        if not _input:
            _input = ""

        op_add_attribute(
            node=maya.selected_object,
            long_name=long_name,
            nice_name=Maya.attribute_nice_name(long_name),
            default_value=_input,
        )
        Maya.select(maya.selected_object)

    @staticmethod
    def add_ac_object():
        maya = RepositoryFacade().maya
        long_name = AttributeType.Object + "_" + "default"
        if Maya.has_attribute(maya.selected_object, long_name):
            print("錯誤: 該屬性已經存在。")
            return
        op_add_attribute(
            node=maya.selected_object,
            long_name=long_name,
            nice_name=Maya.attribute_nice_name(long_name),
            default_value="",
        )
        Maya.select(maya.selected_object)

    @staticmethod
    def add_ac_component():
        maya = RepositoryFacade().maya
        _input = Maya.input_dialog(message="組件名稱 Component 為:")
        if not isinstance(_input, str):
            return
        if not _input:
            _input = "OCMS.Default"
        long_name = (
            AttributeType.Component + "_" + _input.replace(".", "_") + "_" + "default"
        )
        if Maya.has_attribute(maya.selected_object, long_name):
            print("錯誤: 該屬性已經存在。")
            return
        op_add_attribute(
            node=maya.selected_object,
            long_name=long_name,
            nice_name=Maya.attribute_nice_name(long_name),
            default_value="",
        )
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
