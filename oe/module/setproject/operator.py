import oe.tools as tools
import oe.storage as storage

from oe.refer import Registry as reg_


def op_init_project_dir(self):
    tools.Log.set_project_logger().info("Initializing project directory")

    _default_dir = tools.Registry.get_value(
        reg_.REG_KEY, reg_.REG_SUB, reg_.REG_PROJ_DIR, ""
    )
    if _default_dir == "":
        _target_dir = tools.Registry.set_value(
            reg_.REG_KEY,
            reg_.REG_SUB,
            reg_.REG_PROJ_DIR,
            tools.Maya.browser(3, _default_dir),
        )
        self.project_dir_text.lineedit.setText(_target_dir)
    else:
        self.project_dir_text.lineedit.setText(_default_dir)
    self.init_project_dir_btn.set_force_visible(False)
    self.project_dir_text.set_force_visible(True)
    self.project_dir_text.lineedit.setCursorPosition(0)
    self.browse_project_dir_btn.set_force_visible(True)
    # tools.Log.set_project_logger().info("Completed initializing project directory")
    tools.Log.logger(__name__).info("Completed initializing project directory")




def op_browser_project_dir(self):
    tools.Log.set_project_logger().info("Browsing project directory")

    _default_dir = tools.Registry.get_value(
        reg_.REG_KEY, reg_.REG_SUB, reg_.REG_PROJ_DIR, ""
    )
    _browser_dir = tools.Maya.browser(3, _default_dir)
    if _browser_dir == "":
        tools.Log.set_project_logger().warning("User canceled the browser dialog.")
        return
    _target_dir = tools.Registry.set_value(
        reg_.REG_KEY,
        reg_.REG_SUB,
        reg_.REG_PROJ_DIR,
        _browser_dir,
    )
    self.project_dir_text.lineedit.setText(_target_dir)
    self.project_dir_text.lineedit.setCursorPosition(0)
    tools.Log.set_project_logger().info("Completed browsing project directory")
