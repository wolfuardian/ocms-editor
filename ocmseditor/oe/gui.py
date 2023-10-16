from ocmseditor.oe.utils.package import PackageReloader
from ocmseditor.oe.ui.main_decorator import UIMainDecorator

global instance


def show():
    global instance
    PackageReloader.reload(packages=["ocmseditor"])

    try:
        if instance:
            instance.close()
            instance.deleteLater()
            instance = UIMainDecorator()
            instance.update()
            instance.show(dockable=True, area="left")

    except NameError:
        print(f"NameError: {NameError}")
        instance = UIMainDecorator()
        instance.update()
        instance.show(dockable=True, area="left")

    except RuntimeError:
        print(f"RuntimeError: {RuntimeError}")
        instance = UIMainDecorator()
        instance.update()
        instance.show(dockable=True, area="left")
