from ocmseditor import tool
from ocmseditor.oe import ocms
from ocmseditor.core import maya as core
from ocmseditor.oe.data import const as c


def op_fetch(self):
    validate(self)


def op_browser(self):
    core.browser(ocms, tool, c.REG_PROJ_DIR, 3)

    validate(self)


def validate(self):
    _project_dir = ocms.RegistryStore(c.REG_PROJ_DIR).get()

    pre_construct(self, _project_dir)


def pre_construct(self, _project_dir):
    tool.Widget.set_text(self.project_dir_txt.lineedit, _project_dir)
    tool.Widget.show(self.project_dir_txt)
    tool.Widget.show(self.browse_btn)
