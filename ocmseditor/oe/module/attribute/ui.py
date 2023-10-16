from ocmseditor.oe.utils.qt import (
    QtCore,
    QtWidgets,
    QtFloatCSWidget,
    QtScrollareaCSWidget,
    QtFramelessLayoutCSWidget,
    QtGroupVBoxCSWidget,
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
)
from ocmseditor.oe.constant import AttributePanel
from ocmseditor.oe.repository import RepositoryFacade
from .operator import op_set_attr

global instance_edit_attribute


class EditAttributeWidget(QtFramelessLayoutCSWidget):
    def __init__(self):
        super().__init__()
        self.panel_status = AttributePanel.Expanded

        self.container_h_box = QtGroupHBoxCSWidget()
        self.container_h_box.layout.setContentsMargins(0, 0, 0, 0)
        self.container_h_box.layout.setSpacing(0)
        self.container_h_box.setStyleSheet(QtGroupBoxStyle.Transparent)
        self.container_h_box.setFixedHeight(200)

        self.container_collapse_btn = QtButtonCSWidget()
        self.container_collapse_btn.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
        )
        self.container_collapse_btn.setFixedWidth(8)
        self.container_collapse_btn.set_icon(":/nodeGrapherPrevious.png")
        self.container_collapse_btn.setStyleSheet(QtButtonStyle.Dark)

        self.scrollarea = QtScrollareaCSWidget()
        self.scrollarea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.imports_v_box = QtGroupVBoxCSWidget()
        self.imports_v_box.layout.setContentsMargins(0, 0, 0, 0)
        self.imports_v_box.layout.setSpacing(0)
        self.imports_v_box.setStyleSheet(QtGroupBoxStyle.Transparent)
        self.imports_v_box.setFixedWidth(200)
        self.imports_v_box.setFixedHeight(400)

        self.inspector_title_h_box = QtGroupHBoxCSWidget()
        self.inspector_title_h_box.layout.setContentsMargins(0, 0, 0, 0)
        self.inspector_title_h_box.layout.setSpacing(0)
        self.inspector_title_h_box.setStyleSheet(QtGroupBoxStyle.White)

        self.inspector_title = QtHeadingLabelCSWidget()
        self.inspector_title.setText("Inspector")
        self.inspector_title.set_heading(5)
        self.inspector_title.setStyleSheet(QtTitleLabelStyle.Black)

        self.imports_btn_h_box = QtGroupHBoxCSWidget()

        self.imports_btn_h_box.layout.setContentsMargins(0, 0, 0, 0)
        self.imports_btn_h_box.layout.setSpacing(0)
        self.imports_btn_h_box.setStyleSheet(QtGroupBoxStyle.Transparent)

        self.title_h = QtHeadingLabelCSWidget()
        self.title_h.setText("Import From")
        self.title_h.set_heading(5)

        self.edit_attribute = self.create_window()

        self.container_collapse_btn.clicked.connect(self.toggle_panel)

        # self.edit_attribute.layout.setContentsMargins(0, 0, 0, 0)
        # self.edit_attribute.layout.setSpacing(0)

        #
        # self.project_dir_box = QtGroupHBoxCSWidget()
        # self.project_dir_box.set_text("專案路徑")
        #
        # self.fetch_btn = QtButtonCSWidget()
        # self.fetch_btn.setFixedWidth(4)
        # self.fetch_btn.setFixedHeight(16)
        # self.fetch_btn.set_tooltip("Fetch")

        # self.project_dir_txt = qt.QtTextLineCSWidget()
        # self.project_dir_txt.set_text("")
        # self.project_dir_txt.lineedit.setReadOnly(True)
        #
        # self.browse_btn = qt.QtButtonCSWidget()
        # self.browse_btn.set_icon("open_folder.png")
        # self.browse_btn.set_text("")
        # self.browse_btn.setFixedHeight(32)
        #
        # self.fetch_btn.clicked.connect(lambda: operator.op_fetch_project_path(self))
        # self.browse_btn.clicked.connect(lambda: operator.op_browser_project_path(self))
        #
        # self.project_dir_box.layout.addWidget(self.fetch_btn)
        # self.project_dir_box.layout.addWidget(self.project_dir_txt)
        # self.project_dir_box.layout.addWidget(self.browse_btn)
        #
        # self.scrollarea.layout.addWidget(self.project_dir_box)
        #
        # self.frame_layout.addWidget(self.scrollarea)
        #
        # self._validate()
        # self.imports_btn_h_box.layout.addWidget(self.file_btn)
        # self.imports_btn_h_box.layout.addWidget(self.scene_btn)
        #

        self.inspector_title_h_box.layout.addWidget(self.inspector_title)
        self.imports_v_box.layout.addWidget(self.inspector_title_h_box)
        self.scrollarea.layout.addWidget(self.imports_v_box)
        # self.layout().addWidget(self.scrollarea)

        self.container_h_box.layout.addWidget(self.scrollarea)
        self.container_h_box.layout.addWidget(self.container_collapse_btn)

        self.edit_attribute.layout.addWidget(self.container_h_box)

    def toggle_panel(self):
        if self.panel_status == AttributePanel.Expanded:
            self.container_collapse_btn.set_icon(":/nodeGrapherNext.png")
            self.scrollarea.setVisible(False)
            self.panel_status = AttributePanel.Collapsed
        elif self.panel_status == AttributePanel.Collapsed:
            self.container_collapse_btn.set_icon(":/nodeGrapherPrevious.png")
            self.scrollarea.setVisible(True)
            self.panel_status = AttributePanel.Expanded

    def redraw_met_edit_panel(self, context):
        self._destroy_met_edit_panel(context)
        self._construct_met_edit_panel(context)

    def _destroy_met_edit_panel(self, context):
        self.attr_prop_container.clear_all()

    @staticmethod
    def prop_setter(long_name, nice_name, value):
        maya = RepositoryFacade().maya
        op_set_attr(maya.active_object, long_name, value)

    def _construct_met_edit_panel(self, ui):
        for attr_name, attr_value in ui["attrs"].items():
            if isinstance(attr_value, str):
                continue
            elif isinstance(attr_value, dict):
                compound_name = attr_name
                widget = QtGroupVBoxCSWidget()
                widget.setTitle(compound_name)
                self.attr_prop_container.add_group(
                    widget_id=compound_name,
                    widget=widget,
                )
                for _attr_nm, _attr_val in attr_value.items():
                    _prop = QtStringPropertyCSWidget(
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

    @staticmethod
    def create_window():
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
