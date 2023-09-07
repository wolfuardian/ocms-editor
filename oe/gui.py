from maya import cmds

import oe.tools as tools

from oe.ui import ui_tweak

from oe.refer import Product as prod_


global instance


def show():
    global instance
    tools.Log.gui_logger().info(f"Reloading {prod_.ID} packages")
    tools.Packages.reload(packages=["oe"])

    try:
        if instance:
            tools.Log.gui_logger().info("Cleaning existing GUI")
            instance.close()
            instance.deleteLater()
            instance = ui_tweak.Tweak()
            instance.update()
            tools.Log.gui_logger().info("Showing GUI")
            instance.show(dockable=True, area="left")

    except NameError:
        instance = ui_tweak.Tweak()
        tools.Log.gui_logger().warning("NameError")
        tools.Log.gui_logger().info("Showing GUI")
        show()

    except RuntimeError:
        instance = ui_tweak.Tweak()
        tools.Log.gui_logger().warning("RuntimeError")
        tools.Log.gui_logger().info("Showing GUI")
        show()


def undo():
    tools.Log.maya_logger().info("Operating undo")
    cmds.undo()


def redo():
    tools.Log.maya_logger().info("Operating redo")
    cmds.redo()
