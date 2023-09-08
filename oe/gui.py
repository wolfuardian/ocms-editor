from maya import cmds

import oe.tools as tools

from oe.ui import ui_tweak

from oe.utils import const as c


global instance


def show():
    global instance
    tools.Log.info(__name__, f"Reloading {c.PRODUCT_ID} packages")
    tools.Packages.reload(packages=["oe"])

    try:
        if instance:
            tools.Log.info(__name__, "Cleaning existing GUI")
            instance.close()
            instance.deleteLater()
            instance = ui_tweak.Tweak()
            instance.update()
            tools.Log.info(__name__, "Showing GUI")
            instance.show(dockable=True, area="left")

    except NameError:
        instance = ui_tweak.Tweak()
        tools.Log.warning(__name__, "NameError")
        tools.Log.info(__name__, "Showing GUI")
        show()

    except RuntimeError:
        instance = ui_tweak.Tweak()
        tools.Log.warning(__name__, "RuntimeError")
        tools.Log.info(__name__, "Showing GUI")
        show()


def undo():
    tools.Log.info(__name__, "Operating undo")
    cmds.undo()


def redo():
    tools.Log.info(__name__, "Operating redo")
    cmds.redo()
