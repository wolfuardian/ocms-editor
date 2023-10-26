import os
import sys
import pymel.core as pm
import maya.cmds as cmds
import maya.OpenMayaUI as omui

from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from collections import defaultdict

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
    def select(cls, node_name):
        cmds.select(node_name, replace=True)

    @classmethod
    def add_script_job(cls, event):
        return cmds.scriptJob(event=event)

    @classmethod
    def del_script_job(cls, kill, force):
        return cmds.scriptJob(kill=kill, force=force)

    @classmethod
    def get_selected(cls):
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
    def get_attr(cls, node, attr):
        return cmds.getAttr(f"{node}.{attr}")

    @classmethod
    def del_attr(cls, node, attr):
        return cmds.deleteAttr(f"{node}.{attr}")

    @classmethod
    def get_compound_attrs(cls, node_name):
        collect_attrs = {}
        for attr_long, attr_value in cls.get_attrs(node_name).items():
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
    def get_complex_attrs(cls, obj_name):
        attrs = {}
        for attr in cmds.listAttr(obj_name, userDefined=True, write=True) or []:
            children_attrs = cmds.attributeQuery(attr, node=obj_name, listChildren=True)
            if not children_attrs:
                continue
            child_attrs = {}
            for child_attr in children_attrs:
                val = cmds.getAttr(f"{obj_name}.{child_attr}")
                child_attrs[child_attr] = val
            attrs[attr] = child_attrs
        return attrs

    @classmethod
    def add_attr_old(cls, obj_name, compound_attr, attr):
        # if not cmds.attributeQuery(attr, node=obj_name, exists=True):
        #     cmds.addAttr(
        #         obj_name,
        #         longName=parent,
        #         numberOfChildren=10,
        #         attributeType="compound",
        #     )
        #     # cls.add_compound_attr(parent, 10, obj_name)
        # cmds.addAttr(
        #     obj_name,
        #     longName=attr,
        #     niceName=nice_name,
        #     dataType="string",
        #     parent=parent,
        # )
        print(f"compound_attr: {compound_attr}")
        attrs = cls.get_complex_attrs(obj_name)
        attrs[compound_attr][attr] = ""
        cls.add_children_attrs(obj_name, compound_attr, attrs[compound_attr])
        # cls.rename_attr(obj_name, obj_name, obj_name + "aaa")
        #
        # cmds.addAttr(
        #     obj_name,
        #     longName="myCompoundAttr",
        #     numberOfChildren=2,
        #     attributeType="compound",
        # )

        # # 在這個compound屬性下增加兩個子屬性
        # cmds.addAttr(
        #     obj_name, longName="child1", dataType="string", parent="myCompoundAttr"
        # )
        # cmds.addAttr(
        #     obj_name, longName="child2", dataType="string", parent="myCompoundAttr"
        # )

    @classmethod
    def query_attr(cls, node, q_attr):
        attrs = cls.get_attrs(node)
        for attr in attrs.keys():
            if len(attr.split("_")) != 2:
                continue
            if attr.split("_")[0] == q_attr:
                return True
        return False

    @classmethod
    def add_attr(cls, node, attr, default_value=""):
        # 檢查是否重複
        attrs = cls.get_attrs(node)
        for attr_long in attrs.keys():
            parts = attr_long.split("_")
            # if len(parts) == 1:
            #     continue
            if parts[1] == attr:
                Logger.info(__name__, f"已經有 {attr} 屬性了")
                return
        cmds.addAttr(
            node,
            longName=attr,
            niceName=attr.capitalize().replace("_", " | "),
            dataType="string",
        )
        if default_value != "":
            cls.set_attr(node, attr, default_value)

    @classmethod
    def add_compound_attr(cls, node_name, attr_group_name):
        # 標準化
        normalized_name = attr_group_name.lower()

        # 檢查是否重複
        attrs = cls.get_attrs(node_name)
        for attr in attrs.keys():
            if attr.split("_")[0] == normalized_name:
                Logger.info(__name__, f"已經有 {normalized_name} 屬性了")
                return

        attr_name = normalized_name + "_" + "default"
        cmds.addAttr(
            node_name,
            longName=attr_name,
            niceName=attr_name.capitalize().replace("_", " | "),
            dataType="string",
        )

    @classmethod
    def add_children_attrs(cls, obj_name, compound_attr, children_attrs):
        cmds.deleteAttr(f"{obj_name}.{compound_attr}")
        cmds.addAttr(
            obj_name,
            longName=compound_attr,
            numberOfChildren=len(children_attrs),
            attributeType="compound",
        )
        cmds.addAttr(
            obj_name,
            longName=compound_attr + "aaa",
            dataType="string",
            parent=compound_attr,
        )
        print(f"num_children_attrs: {len(children_attrs)}")
        aattrs = cls.get_complex_attrs(obj_name)
        print(f"aattrs: {aattrs}")

        # for attr, attr_value in children_attrs.items():
        #     print(f"attr={attr}, attr_value={attr_value}")
        #     print(f"obj_name = {obj_name}")
        #     attr: str
        #     a = cmds.addAttr(
        #         obj_name,
        #         longName=attr,
        #         niceName=attr.replace(compound_attr, ""),
        #         dataType="string",
        #         parent=compound_attr,
        #     )
        #     print(f"a = {a}")
        #     # aattrs = cls.get_attrs(obj_name)
        #     # print(f"attrs = {aattrs}")
        #     # ch_attrs = cmds.attributeQuery(attr, node=obj_name, listChildren=True) or []
        #     # print(f"ch_attrs = {ch_attrs}")
        #     # cmds.setAttr(f"{obj_name}.{attr}", attr_value, type="string")
        #     # cls.set_attr(obj_name, attr, attr_value)

    @classmethod
    def set_attr(cls, node, attr, attr_value):
        cmds.setAttr(f"{node}.{attr}", attr_value, type="string")

    @classmethod
    def del_compound_attr(cls, obj_name, compound_attr_name):
        cmds.deleteAttr(f"{obj_name}.{compound_attr_name}")

    @classmethod
    def rename_attr(cls, node, old_attr_name, new_attr_name):
        # Copy the old value
        old_value = cmds.getAttr(f"{node}.{old_attr_name}")

        # Add new attribute
        cmds.addAttr(node, longName=new_attr_name, dataType="string")

        # Set the value of the new attribute to the old value
        cmds.setAttr(f"{node}.{new_attr_name}", old_value)

        # Delete the old attribute
        cmds.deleteAttr(f"{node}.{old_attr_name}")

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
