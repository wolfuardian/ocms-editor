from ocmseditor.oe.constant import ICON_DIR
from ocmseditor.oe.utils.qt import (
    QtGui,
    QtScrollareaCSWidget,
    QtFramelessLayoutCSWidget,
    QtGroupVBoxCSWidget,
    QtGroupHBoxCSWidget,
    QtHeadingLabelCSWidget,
    QtButtonCSWidget,
    QtBigButtonCSWidget,
    QtDefaultCSWidget,
)
from ocmseditor.oe.utils.qt_stylesheet import QtGroupBoxStyle, QtButtonStyle
from ocmseditor.oe.constant import INFO__BROWSER_CANCELED

from ocmseditor.oe.repository import RepositoryFacade

import ocmseditor.tool as tool


class ImportsWidget(QtFramelessLayoutCSWidget):
    def __init__(self):
        super().__init__()

        # self.set_text("編輯屬性")

        self.scrollarea = QtScrollareaCSWidget()

        self.imports_v_box = QtGroupVBoxCSWidget()
        self.imports_v_box.layout.setContentsMargins(10, 10, 10, 10)
        self.imports_v_box.layout.setSpacing(10)
        self.imports_v_box.setStyleSheet(QtGroupBoxStyle.Transparent)
        self.imports_btn_h_box = QtGroupHBoxCSWidget()

        self.imports_btn_h_box.layout.setContentsMargins(0, 0, 0, 0)
        self.imports_btn_h_box.layout.setSpacing(0)
        self.imports_btn_h_box.setStyleSheet(QtGroupBoxStyle.Transparent)
        # self.imports_btn_h_box.set_text("專案路徑")

        self.title_h = QtHeadingLabelCSWidget()
        self.title_h.setText("Import From")
        self.title_h.set_heading(3)
        self.file_btn = QtBigButtonCSWidget()
        self.file_btn.setText("Files")
        self.file_btn.set_icon("file.png")
        self.file_btn.setFixedWidth(100)
        self.file_btn.setFixedHeight(100)
        self.file_btn.setStyleSheet(QtButtonStyle.Big)
        self.scene_btn = QtBigButtonCSWidget()
        self.scene_btn.setText("Scene")
        self.scene_btn.set_icon("cube.png")
        self.scene_btn.setFixedWidth(100)
        self.scene_btn.setFixedHeight(100)
        self.scene_btn.setStyleSheet(QtButtonStyle.Big)

        self.file_btn.clicked.connect(
            lambda: self.on_file_btn_clicked(context=RepositoryFacade().ui.main)
        )
        self.scene_btn.clicked.connect(
            lambda: self.on_scene_btn_clicked(context=RepositoryFacade().ui.main)
        )

        # main_ui = Repository().ui.main
        # print(main_ui)

        #
        # self.fetch_btn = qt.QtButtonCSWidget()
        # self.fetch_btn.setFixedWidth(4)
        # self.fetch_btn.setFixedHeight(16)
        # self.fetch_btn.set_tooltip("Fetch")
        #
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
        self.imports_btn_h_box.layout.addWidget(self.file_btn)
        self.imports_btn_h_box.layout.addWidget(self.scene_btn)
        self.imports_v_box.layout.addWidget(self.title_h)
        self.imports_v_box.layout.addWidget(self.imports_btn_h_box)
        self.scrollarea.layout.addWidget(self.imports_v_box)
        self.layout().addWidget(self.scrollarea)

        # self._validate()

    @staticmethod
    def on_file_btn_clicked(context):
        from ocmseditor.oe.ui.main import UIMain

        browser_dir = tool.Maya.browser(1)
        if browser_dir == INFO__BROWSER_CANCELED:
            return

        print(f"browser_dir = {browser_dir}")

        context: UIMain
        context.tab_bar.setTabEnabled(0, False)
        context.switch_to_file_mode()

    @staticmethod
    def on_scene_btn_clicked(context):
        from ocmseditor.oe.ui.main import UIMain

        context: UIMain
        context.tab_bar.setTabEnabled(0, False)
        context.switch_to_scene_mode()
