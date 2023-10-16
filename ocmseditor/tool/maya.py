import os
import sys
import pymel.core as pm
import maya.cmds as cmds
import maya.OpenMayaUI as omui

from PySide2 import QtWidgets
from shiboken2 import wrapInstance

from ocmseditor.oe.utils.logger import Logger
from ocmseditor.oe.constant import INFO__BROWSER_CANCELED

from PySide2 import QtWidgets, QtCore, QtGui

import ocmseditor.core.tool as core


class Maya(core.Maya):
    @classmethod
    def browser(
        cls,
        file_mode,
        default_dir="",
        file_filter="All Files (*.*)",
    ):
        """
        調用Maya的文件對話框來選擇文件或文件夾。

        參數:
            file_mode (int): 指定文件對話框的返回類型。有效值為 0-4。
            default_dir (str): 指定對話框打開時的默認目錄。默認值為用戶的家目錄。
            file_filter (str): 指定在對話框中可選擇的文件類型。

        File Mode:
            0 任何文件，無論是否存在。
            1 單個現有文件。
            2 目錄的名稱。目錄和文件都顯示在對話框中。
            3 目錄的名稱。只有目錄顯示在對話框中。
            4 現有文件的名稱。

        範例:
            path = YourClass.browser(1, default_dir='/some/dir', file_filter="Maya Files (*.maya *.mb)")

        返回:
            選擇的文件或文件夾的路徑，或者如果用戶取消操作，則返回False。
        """

        try:
            return pm.fileDialog2(
                fileMode=file_mode, dir=default_dir, fileFilter=file_filter
            )[0]
        except TypeError:
            Logger.info(__name__, INFO__BROWSER_CANCELED)
            return INFO__BROWSER_CANCELED

    @classmethod
    def add_script_job(cls, event):
        return cmds.scriptJob(event=event)

    @classmethod
    def del_script_job(cls, kill, force):
        return cmds.scriptJob(kill=kill, force=force)

    @classmethod
    def get_active_object(cls):
        return cmds.ls(selection=True)

    @classmethod
    def get_active_viewport(cls):
        panels = cmds.getPanel(type="modelPanel")
        print(f"panels: {panels}")
        if not panels:
            return None

        panel = panels[0]

        ptr = omui.MQtUtil.findControl(panel)
        print(f"ptr: {ptr}")
        if ptr is None:
            return None

        inst = wrapInstance(int(ptr), QtWidgets.QWidget)
        print(f"inst: {inst}")
        geom = inst.geometry()
        # print(f"geom: {geom}")
        # QtCore.QCoreApplication.processEvents()
        # aaa = QtCore.QTimer.singleShot(1000, lambda: inst.mapToGlobal(geom.topLeft()))
        # print(f"aaa: {aaa}")
        #
        # global_point = inst.mapToGlobal(geom.topLeft())
        # print(f"global_point: {global_point}")
        return wrapInstance(int(ptr), QtWidgets.QWidget)

    @classmethod
    def get_global_point(cls, inst):
        geom = inst.geometry()
        global_point = inst.mapToGlobal(geom.topLeft())
        print(f"global_point: {global_point}")
        return global_point

    @classmethod
    def get_global_point_delay(cls, inst):
        return QtCore.QTimer.singleShot(
            500, lambda: cls.get_global_point(inst)
        )
