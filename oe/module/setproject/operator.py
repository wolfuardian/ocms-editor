import oe.tools as tools
import oe.storage as storage
import oe.core.maya as core

from oe.utils import const as c


def op_fetch_project_dir(self):
    tools.Log.info(__name__, "Fetching project directory")

    validate_project_dir(self)


def op_init_project_dir(self):
    tools.Log.info(__name__, "Initializing project directory")

    op_browser_project_dir(self)


def op_browser_project_dir(self):
    tools.Log.info(__name__, "Browsing project directory")

    sel_path = core.browser(storage, tools, c.REG_PROJ_DIR, 3)

    validate_project_dir(self)

    storage.Widget(self.project_dir_txt.lineedit).set_text(sel_path)

    storage.Widget(self.project_dir_txt).show()
    storage.Widget(self.init_btn).hide()
    storage.Widget(self.browse_btn).show()


def validate_project_dir(self):
    tools.Log.info(__name__, "Validating project directory")

    _project_dir = storage.Registry(c.REG_PROJ_DIR).get()
    if (
        not storage.Path(_project_dir).is_valid()
        or not storage.Path(_project_dir).is_dir()
    ):
        # TODO: Check if project directory is invalid
        pass
    else:
        # TODO: Check if project directory is valid
        pass

    _setup_ui(self, _project_dir)


def _setup_ui(self, _project_dir):
    tools.Log.info(__name__, "Setting up project directory ui")

    storage.Widget(self.project_dir_txt.lineedit).set_text(_project_dir)
    storage.Widget(self.project_dir_txt).show()
    storage.Widget(self.init_btn).hide()
    storage.Widget(self.browse_btn).show()
