import os
import sys
import pymel.core as pm
import maya.cmds as cmds
import maya.OpenMayaUI as omui

from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from collections import defaultdict

from ocmseditor.oe.utils.logger import Logger
from ocmseditor.oe.constant import INFO__BROWSER_CANCELED, AttributeType

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
    def select(cls, node_name):
        cmds.select(node_name, replace=True)

    @classmethod
    def add_script_job(cls, event):
        return cmds.scriptJob(event=event)

    @classmethod
    def del_script_job(cls, kill, force):
        return cmds.scriptJob(kill=kill, force=force)

    @classmethod
    def get_selected_object(cls):
        return cmds.ls(selection=True)

    @classmethod
    def get_active_viewport(cls):
        panels = cmds.getPanel(type="modelPanel")
        if not panels:
            return None
        panel = panels[0]
        ptr = omui.MQtUtil.findControl(panel)
        if ptr is None:
            return None
        try:
            return wrapInstance(int(ptr), QtWidgets.QWidget)
        except Exception as e:
            print("Failed to wrap instance: {}".format(e))
            return None

    @classmethod
    def get_attrs(cls, node_name):
        attrs = {}
        for attr in cmds.listAttr(node_name, userDefined=True, write=True) or []:
            if not cmds.attributeQuery(attr, node=node_name, numberOfChildren=True):
                attrs[attr] = cmds.getAttr(f"{node_name}.{attr}")
        return attrs

    @classmethod
    def get_attr_type(cls, attr):
        parts = attr.split("_")
        if len(parts) == 2:
            return AttributeType.Simple
        if len(parts) >= 3:
            return AttributeType.Complex
        return AttributeType.Undefined

    @classmethod
    def get_attrs_hierarchy(cls, node):
        collect_attrs = {}
        for attr_long, attr_value in cls.get_attrs(node).items():
            print(f"attr_long, attr_value: {attr_long}, {attr_value}")
            parts = attr_long.split("_")
            if len(parts) == 1:
                # 沒有屬性組的時候
                compound_attr = "_"
                attr = parts[0]
            else:
                compound_attr = parts[0]
                attr = parts[1]
            if collect_attrs.get(compound_attr) is None:
                collect_attrs[compound_attr] = {}
            collect_attrs[compound_attr][attr] = attr_value
        return collect_attrs

    @classmethod
    def get_attr(cls, node, attr):
        return cmds.getAttr(f"{node}.{attr}")

    @classmethod
    def del_attr(cls, node, attr):
        return cmds.deleteAttr(f"{node}.{attr}")

    @classmethod
    def add_attr_old(cls, node, attr, default_value=""):
        cmds.addAttr(
            node,
            longName=attr,
            niceName=attr.capitalize().replace("_", " | "),
            dataType="string",
        )
        if default_value != "":
            cls.set_attr(node, attr, default_value)

    @classmethod
    def add_attr(cls, node, compound, attr, default_value=""):
        long_name = compound + "_" + attr
        cmds.addAttr(
            node,
            longName=long_name,
            niceName=long_name.capitalize().replace("_", " | "),
            dataType="string",
        )
        if default_value != "":
            cls.set_attr(node, long_name, default_value)

    @classmethod
    def add_ac_object(cls, node, attr_compound):
        cls.add_attr(node, attr_compound, "default")

    @classmethod
    def add_ac_component(cls, node, attr_compound):

        pass

    @classmethod
    def set_attr(cls, node, attr, attr_value):
        cmds.setAttr(f"{node}.{attr}", attr_value, type="string")

    @classmethod
    def user_input_dialog(cls, title="輸入框", message="請輸入:"):
        result = cmds.promptDialog(
            title=title,
            message=message,
            button=["確定", "取消"],
            defaultButton="確定",
            cancelButton="取消",
            dismissString="取消",
        )

        if result == "確定":
            text = cmds.promptDialog(query=True, text=True)
            return text
        else:
            return None
