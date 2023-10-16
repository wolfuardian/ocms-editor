from ocmseditor.oe.utils.qt import (
    QtFloatCSWidget,
    QtScrollareaCSWidget,
    QtFramelessLayoutCSWidget,
    QtGroupVBoxCSWidget,
    QtGroupHBoxCSWidget,
    QtGroupHBoxCSWidget,
    QtHeadingLabelCSWidget,
    QtButtonCSWidget,
    get_main_window,
)
from ocmseditor.oe.utils.qt_stylesheet import (
    QtGroupBoxStyle,
    QtButtonStyle,
    QtTitleLabelStyle,
)

global instance_attribute_panel


class EditAttributeWidget(QtFramelessLayoutCSWidget):
    def __init__(self):
        super().__init__()
        self.scrollarea = QtScrollareaCSWidget()

        self.imports_v_box = QtGroupVBoxCSWidget()
        self.imports_v_box.layout.setContentsMargins(0, 0, 0, 0)
        self.imports_v_box.layout.setSpacing(0)
        self.imports_v_box.setStyleSheet(QtGroupBoxStyle.Transparent)

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

        self.attribute_panel = self.create_attribute_panel()
        self.attribute_panel.layout.setContentsMargins(0, 0, 0, 0)
        self.attribute_panel.layout.setSpacing(0)
        self.attribute_panel.setFixedWidth(150)
        self.attribute_panel.setFixedHeight(600)

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
        self.layout().addWidget(self.scrollarea)

        self.attribute_panel.layout.addWidget(self.scrollarea)

    @staticmethod
    def create_attribute_panel():
        global instance_attribute_panel
        try:
            if instance_attribute_panel:
                instance_attribute_panel.close()
                instance_attribute_panel.deleteLater()
                instance_attribute_panel = QtFloatCSWidget(parent=get_main_window())
                instance_attribute_panel.update()
                instance_attribute_panel.show()

        except NameError:
            print(f"NameError: {NameError}")
            instance_attribute_panel = QtFloatCSWidget(parent=get_main_window())
            instance_attribute_panel.update()
            instance_attribute_panel.show()

        except RuntimeError:
            print(f"RuntimeError: {RuntimeError}")
            instance_attribute_panel = QtFloatCSWidget(parent=get_main_window())
            instance_attribute_panel.update()
            instance_attribute_panel.show()
        return instance_attribute_panel
