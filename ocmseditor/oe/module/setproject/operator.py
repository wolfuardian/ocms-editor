import ocmseditor.tool as tool
import ocmseditor.oe.helper as helper
import ocmseditor.oe.data.const as const


def op_fetch_project_path(self):
    helper.Logger.info(__name__, "Fetching project path")
    # Operator: Fetch -> Validate
    self._validate()


def op_browser_project_path(self):
    helper.Logger.info(__name__, "Browsing project path")
    # Operator: Browser -> Validate
    default_path = tool.Registry.get_reg(const.REG_PROJ_PATH)
    folder_path = tool.Maya.browser(3, default_path, "All Folders (*.*)")
    if not folder_path:
        return
    tool.Registry.set_reg(const.REG_PROJ_PATH, folder_path)
    self._validate()
