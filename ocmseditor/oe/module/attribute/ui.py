from ocmseditor.oe.utils.qt import (
    QtCore,
    QtWidgets,
    QtResizeCSWidget,
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
from ocmseditor.oe.constant import AttributePanel
from ocmseditor.oe.repository import RepositoryFacade
from .operator import op_set_attr

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
        self.__container_h_box.setFixedHeight(280)

        self.__container_h_box.set_resizeable = True
        self.__container_h_box.sizeSetter.connect(self.resize_widget)
        self.__container_h_box.setStyleSheet(QtGroupBoxStyle.Transparent)

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

        self.__inspector_title_h_box = QtGroupHBoxCSWidget()
        self.__inspector_title_h_box.layout.setContentsMargins(0, 0, 0, 0)
        self.__inspector_title_h_box.layout.setSpacing(0)
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


    def resize_widget(self, size):
        self.__container_h_box.setFixedHeight(size.height())

    def toggle_panel(self):
        if self.panel_status == AttributePanel.Expanded:
            self.__container_collapse_btn.set_icon(":/nodeGrapherNext.png")
            self.__container_v_box.setVisible(False)
            self.panel_status = AttributePanel.Collapsed
        elif self.panel_status == AttributePanel.Collapsed:
            self.__container_collapse_btn.set_icon(":/nodeGrapherPrevious.png")
            self.__container_v_box.setVisible(True)
            self.panel_status = AttributePanel.Expanded

    def redraw_edit_attributes(self, attrs):
        self.destroy_edit_attributes()
        self.construct_edit_attributes(attrs)

    def destroy_edit_attributes(self):
        self.__attributes_props_v_container.clear_all()

    def construct_edit_attributes(self, attrs: dict):
        for compound_attr, children_attrs in attrs.items():
            __group = QtGroupVBoxCSWidget(title=compound_attr)
            __group.setStyleSheet(QtGroupBoxStyle.Minimal)

            self.__attributes_props_v_container.add_group(
                group_id=compound_attr, widget=__group
            )
            for attr, attr_value in children_attrs.items():
                __prop = QtStringPropertyCSWidget(
                    long_name=compound_attr + "." + attr,
                    nice_name=attr.capitalize(),
                    value=attr_value,
                )
                __prop.setStyleSheet(QtPropertyStyle.Minimal)
                self.__attributes_props_v_container.add_widget(
                    group_id=compound_attr, widget_id=attr, widget=__prop
                )
                __prop.lineedit.setCursorPosition(0)
                __prop.propertySetter.connect(self.prop_setter)

    @staticmethod
    def prop_setter(attr, nice_name, value):
        maya = RepositoryFacade().maya
        op_set_attr(maya.active_object, attr, value)

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
