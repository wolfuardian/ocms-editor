import oe.tools as tools
import oe.storage as storage

from oe.refer import Registry as reg


def op_init_project_dir(self):
    tools.Log.info(__name__, "Initializing project directory")

    op_browser_project_dir(self)


def op_browser_project_dir(self):
    tools.Log.info(__name__, "Browsing project directory")

    sel_path = Operator.browser()

    Widget(self.project_dir_txt.lineedit).update_txt(sel_path)

    Widget(self.init_project_dir_btn).hide()
    Widget(self.project_dir_txt).show()
    Widget(self.browse_project_dir_btn).show()


def validate_project_dir(self):
    _project_dir = storage.Registry(reg.REG_PROJ_DIR).get()
    if not storage.Path(_project_dir).is_valid():
        return

    _setup_project_dir_ui(self, _project_dir)


def _setup_project_dir_ui(self, _project_dir):
    Widget(self.project_dir_txt.lineedit).update_txt(_project_dir)
    Widget(self.project_dir_txt).show()
    Widget(self.init_project_dir_btn).hide()
    Widget(self.browse_project_dir_btn).show()


class Operator:
    @classmethod
    def browser(cls):
        _default = storage.Registry(reg.REG_PROJ_DIR).get()

        _browser = tools.Maya.browser(3, _default)
        if _browser == "":
            tools.Log.warning(__name__, "User canceled the browser dialog.")
            return _default

        return storage.Registry(reg.REG_PROJ_DIR).set(_browser)


class Widget:
    def __init__(self, widget):
        self.widget = widget

    def hide(self):
        self.widget.set_force_visible(False)

    def show(self):
        self.widget.set_force_visible(True)

    def update_txt(self, text):
        self.widget.setText(text)
        self.widget.setCursorPosition(0)
