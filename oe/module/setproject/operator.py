import oe.tools as tools
import oe.storage as storage
import oe.core.maya as core

from oe.utils import const as c


def op_init_project_dir(self):
    tools.Log.info(__name__, "Initializing project directory")

    op_browser_project_dir(self)


def op_browser_project_dir(self):
    tools.Log.info(__name__, "Browsing project directory")

    sel_path = core.browser(storage, tools, c.REG_PROJ_DIR, 3)

    storage.Widget(self.project_dir_txt.lineedit).set_text(sel_path)

    storage.Widget(self.project_dir_txt).show()
    storage.Widget(self.init_project_dir_btn).hide()
    storage.Widget(self.browse_project_dir_btn).show()


def validate_project_dir(self):
    _project_dir = storage.Registry(c.REG_PROJ_DIR).get()
    if not storage.Path(_project_dir).is_valid():
        return

    _setup_project_dir_ui(self, _project_dir)


def _setup_project_dir_ui(self, _project_dir):
    storage.Widget(self.project_dir_txt).set_text(_project_dir)
    storage.Widget(self.project_dir_txt).show()
    storage.Widget(self.init_project_dir_btn).hide()
    storage.Widget(self.browse_project_dir_btn).show()
