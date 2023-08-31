import re
from maya import cmds

from . import store
import oe.tools as tools

from refer import Registry as reg_

def op_browser_project_dir():
    tools.Logging.operator_logger().info("Browsing project directory")

    _default_dir = tools.Registry.get_value(reg_.REG_KEY, reg_.REG_SUB, "Pref_ProjectDirectory", "")
    if len(_default_dir) > 0:
        _val = tools.Registry.set_value(reg_.REG_KEY, reg_.REG_SUB, "Pref_ProjectDirectory", tools.Maya.browser(3, _default_dir))

        le.setText(_val)
        le.setCursorPosition(0)


