from maya import cmds
from oe.ui import ui_tweak

import oe.tools as tools
from version import version as ver

global instance

mod = ver.split("-")[0] + "-" + ver.split("-")[1]

def show():
    global instance
    tools.Logging.gui_logger().info(f"Reloading {mod} packages")
    tools.Packages.reload(packages=["oe"])

    try:
        if instance:
            tools.Logging.gui_logger().info("Closing GUI")
            instance.close()
            instance.deleteLater()
            instance = ui_tweak.Tweak()
            instance.update()
            tools.Logging.gui_logger().info("Showing GUI")
            instance.show(dockable=True, area='left')

    except NameError:
        instance = ui_tweak.Tweak()
        tools.Logging.gui_logger().warning("NameError")
        tools.Logging.gui_logger().info("Showing GUI")
        show()

    except RuntimeError:
        instance = ui_tweak.Tweak()
        tools.Logging.gui_logger().warning("RuntimeError")
        tools.Logging.gui_logger().info("Showing GUI")
        show()


def undo():
    tools.Logging.maya_logger().info("Operating undo")
    cmds.undo()


def redo():
    tools.Logging.maya_logger().info("Operating redo")
    cmds.redo()
