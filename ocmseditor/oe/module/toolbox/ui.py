import ocmseditor.oe.qt as qt
import ocmseditor.tool as tool
import ocmseditor.oe.helper as helper
import ocmseditor.oe.data.const as const

from . import operator


class ToolBoxCSWidget(qt.QtGroupHBoxCSWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.import_xml = False
        self.write_xml = False
        self.import_res = False

        self.layout.setContentsMargins(0, 0, 0, 0)

        self.set_status(qt.QtGroupBoxStatus.Transparent)
        self.setFixedHeight(64)

        self.tool_box = qt.QtGroupVBoxCSWidget()
        self.tool_box.layout.setContentsMargins(0, 0, 0, 0)

        self.import_xml_btn = qt.QtButtonCSWidget()
        self.import_xml_btn.set_icon(":/inArrow.png")
        self.import_xml_btn.set_text("  匯入 XML")
        self.import_xml_btn.set_status(qt.QtButtonStatus.Transparent)
        self.import_xml_btn.setSizePolicy(
            qt.QtWidgets.QSizePolicy.Expanding, qt.QtWidgets.QSizePolicy.Expanding
        )

        self.import_res_btn = qt.QtButtonCSWidget()
        self.import_res_btn.set_icon(":/teImport.svg")
        self.import_res_btn.set_text("  匯入 Resource")
        self.import_res_btn.set_status(qt.QtButtonStatus.Transparent)
        self.import_res_btn.setSizePolicy(
            qt.QtWidgets.QSizePolicy.Expanding, qt.QtWidgets.QSizePolicy.Expanding
        )

        self.write_xml_btn = qt.QtButtonCSWidget()
        self.write_xml_btn.set_icon(":/outArrow.png")
        self.write_xml_btn.set_text("  匯出 XML")
        self.write_xml_btn.set_status(qt.QtButtonStatus.Transparent)
        self.write_xml_btn.setSizePolicy(
            qt.QtWidgets.QSizePolicy.Expanding, qt.QtWidgets.QSizePolicy.Expanding
        )

        self.import_res_btn.clicked.connect(lambda: operator.op_import_resource(self))

        self.tool_box.layout.addWidget(self.import_xml_btn)
        self.tool_box.layout.addWidget(self.write_xml_btn)

        self.layout.addWidget(self.tool_box)
        self.layout.addWidget(self.import_res_btn)

        self._validate()

    def _validate(self):
        helper.Logger.info(__name__, "Validating resource directory")

        self.import_xml_btn.setEnabled(self.import_xml)
        self.write_xml_btn.setEnabled(self.write_xml)
        self.import_res_btn.setEnabled(self.import_res)
