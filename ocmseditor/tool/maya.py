import os
import sys
import pymel.core as pm
import maya.cmds as cmds
import maya.OpenMayaUI as omui

from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from collections import defaultdict

from ocmseditor.oe.utils.logger import Logger
from ocmseditor.oe.constant import INFO__BROWSER_CANCELED, Attribute, AttributeType

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
    def get_attributes(cls, node):
        result = defaultdict(dict)
        for attr in cmds.listAttr(node, userDefined=True, write=True) or []:
            if not cmds.attributeQuery(attr, node=node, numberOfChildren=True):
                result[attr] = cmds.getAttr(f"{node}.{attr}")
        return dict(result)

    @classmethod
    def has_attribute(cls, node, attribute):
        return cmds.attributeQuery(attribute, node=node, exists=True)

    @classmethod
    def parse_attributes(cls, attributes):
        result = defaultdict(dict)
        for attribute, value in attributes.items():
            parsed_attribute = cls.parse_attribute(attribute, value)
            result.update(parsed_attribute)
        return dict(result)

    @classmethod
    def parse_attribute(cls, attribute, value):
        attr_data = {
            Attribute.LongName: attribute,
            Attribute.ShortName: cls.attribute_short_name(attribute),
            Attribute.NiceName: cls.attribute_nice_name(attribute),
            Attribute.Type: cls.attribute_type(attribute),
            Attribute.Compound: cls.attribute_compound(attribute),
            Attribute.StringProperty: value,
        }
        result = {attribute: attr_data}
        return result

    @classmethod
    def attribute_type(cls, attribute):
        parts = attribute.split("_")
        first_part = parts[0]
        if len(parts) == 2 and first_part == AttributeType.Object:
            return AttributeType.Object
        if len(parts) >= 3 and first_part == AttributeType.Component:
            return AttributeType.Component
        return AttributeType.Undefined

    @classmethod
    def attribute_compound(cls, attribute):
        head, body, tail = cls.split_attribute(attribute)
        return body

    @classmethod
    def attribute_short_name(cls, attribute):
        head, body, tail = cls.split_attribute(attribute)
        return tail

    @classmethod
    def attribute_nice_name(cls, attribute):
        head, body, tail = cls.split_attribute(attribute)
        typ = cls.attribute_type(attribute)
        if not body:
            body = head
        head = typ
        body = body.replace("_", ".")
        if typ == AttributeType.Component:
            nice_name = " | ".join([head, body, tail])
        else:
            nice_name = " | ".join([head, tail])
        return nice_name

    @classmethod
    def sort_parsed_attributes(cls, parsed_attributes):
        result = defaultdict(dict)
        for attribute, attr_data in parsed_attributes.items():
            typ, cp, ln = (
                attr_data.get(Attribute.Type),
                attr_data.get(Attribute.Compound),
                attr_data.get(Attribute.LongName),
            )
            if cp not in result[typ]:
                result[typ][cp] = defaultdict(dict)
            result[typ][cp][ln] = attr_data
        return dict(result)

    @classmethod
    def split_attribute(cls, attribute):
        parts = attribute.split("_")
        has_body = len(parts) >= 3
        parts_head = parts[0]
        if has_body:
            parts_body = parts[1:-1]
        else:
            parts_body = []
        parts_tail = parts[-1]
        head, body, tail = parts_head, ".".join(parts_body), parts_tail

        typ = cls.attribute_type(attribute)
        if not body:
            body = head
        head = typ

        return head, body, tail

    @classmethod
    def get_attribute(cls, node, attr):
        return cmds.getAttr(f"{node}.{attr}")

    @classmethod
    def del_attribute(cls, node, attr):
        return cmds.deleteAttr(f"{node}.{attr}")

    @classmethod
    def add_attribute(cls, node, long_name, nice_name="", default_value=""):
        if nice_name == "":
            nice_name = long_name.replace("_", " | ")
        cmds.addAttr(
            node,
            longName=long_name,
            niceName=nice_name,
            dataType="string",
        )
        if default_value != "":
            cls.set_attribute(node, long_name, default_value)

    @classmethod
    def set_attribute(cls, node, attr, attr_value):
        cmds.setAttr(f"{node}.{attr}", attr_value, type="string")

    @classmethod
    def input_dialog(cls, title="輸入框", message="請輸入:"):
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
