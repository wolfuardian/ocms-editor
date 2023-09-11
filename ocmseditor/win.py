from ocmseditor import tool

from ocmseditor.oe import ui

global instance


def show():
    global instance
    tool.Packages.reload(packages=["ocmseditor"])

    try:
        if instance:
            instance.close()
            instance.deleteLater()
            instance = ui.Tweak()
            instance.update()
            instance.show(dockable=True, area="left")

    except NameError:
        instance = ui.Tweak()
        show()

    except RuntimeError:
        instance = ui.Tweak()
        show()
