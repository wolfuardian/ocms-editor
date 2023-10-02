import os
import sys
import pymel.core as pm
import maya.cmds as cmds
import maya.OpenMayaUI as omui

from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import ocmseditor.core.tool as core
import ocmseditor.oe.helper as helper


class Maya(core.Maya):
    @classmethod
    def get_main_window(cls):
        """
        獲取Maya的主窗口並將其轉換為PyQt的QWidget對象。

        參數:
            無。

        範例:
            main_window = YourClass.get_main_window()  # 返回Maya主窗口的QWidget對象

        返回:
            Maya主窗口的QWidget對象。
        """
        maya_main_ptr = omui.MQtUtil.mainWindow()
        if sys.version_info.major >= 3:
            return wrapInstance(int(maya_main_ptr), QtWidgets.QWidget)
        else:
            return wrapInstance(long(maya_main_ptr), QtWidgets.QWidget)

    @classmethod
    def browser(
        cls,
        file_mode,
        default_dir=os.path.expanduser("~"),
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
            path = YourClass.browser(1, default_dir='/some/dir', file_filter="Maya Files (*.ma *.mb)")

        返回:
            選擇的文件或文件夾的路徑，或者如果用戶取消操作，則返回False。
        """

        try:
            browser_path = pm.fileDialog2(
                fileMode=file_mode, dir=default_dir, fileFilter=file_filter
            )[0]
            return browser_path
        except TypeError:
            helper.Logger.info(__name__, "Browser canceled")
            return False

    @classmethod
    def import_file(cls, path, typ="FBX"):
        """
        在Maya場景中導入指定類型的文件。

        參數:
            path: str
                文件的絕對或相對路徑。
            typ: str, 可選
                文件的類型，預設為"FBX"。

        範例:
            new_nodes = YourClass.import_file("C:/path/to/your/file.fbx")

        返回:
            一個包含新添加節點的名稱列表。
        """
        return cmds.file(
            path,
            i=True,
            force=True,
            type=typ,
            ignoreVersion=True,
            mergeNamespacesOnClash=True,
            returnNewNodes=True,
        )

    @classmethod
    def uuid(cls, obj_name):
        """
        獲取Maya場景中特定對象的唯一識別符（UUID）。

        參數:
            obj_name: str
                Maya場景中的對象名稱。

        範例:
            unique_id = YourClass.uuid("pCube1")  # 返回對象 "pCube1" 的UUID

        返回:
            對象的UUID。
        """
        return cmds.ls(obj_name, uuid=True)[0]

    @classmethod
    def get_selected(cls):
        """
        獲取Maya場景中當前選擇的所有物件。

        範例:
            selected_objects = YourClass.get_selected()

        返回:
            包含所有當前選擇物件名稱的列表。
        """
        return cmds.ls(selection=True)

    @classmethod
    def get_top_level_transforms(cls):
        """
        獲取Maya場景中的根節點。

        範例:
            root_node = YourClass.get_root_node()

        返回:
            根節點的名稱。
        """
        top_level_transforms = [
            node
            for node in cmds.ls(type="transform")
            if not cmds.listRelatives(node, parent=True)
        ]
        return top_level_transforms

    @classmethod
    def obj_exists(cls, obj_name):
        """
        檢查指定的對象是否存在。

        參數:
            obj_name: 要檢查的對象的名稱。

        範例:
            exists = YourClass.obj_exists("objName")

        返回:
            如果對象存在，返回 True；否則返回 False。
        """
        return cmds.objExists(obj_name)

    @classmethod
    def attr_exists(cls, attr_name, obj_name):
        """
        檢查指定對象上是否存在給定的屬性。

        參數:
            attr_name: 要檢查的屬性的名稱。
            obj_name: 對象的名稱。

        範例:
            exists = YourClass.attr_exists("attributeName", "objName")

        返回:
            如果屬性存在，返回 True；否則返回 False。
        """
        return cmds.attributeQuery(attr_name, node=obj_name, exists=True)

    @classmethod
    def add_compound_attr(cls, attr_name, child_count, obj_name):
        """
        在指定的對象上添加一個新的複合屬性。

        參數:
            attr_name: 要添加的复合屬性的名稱。
            child_count: 复合屬性下的子屬性數量。
            obj_name: 對象的名稱。

        範例:
            YourClass.add_compound_attr("compoundAttr", 3, "objName")

        返回:
            無。
        """
        cmds.addAttr(
            obj_name,
            longName=attr_name,
            numberOfChildren=child_count,
            attributeType="compound",
        )

    @classmethod
    def add_string_child_attr(cls, attr_name, parent_attr_name, obj_name):
        """
        在指定對象上添加一個新的字符串子屬性。

        參數:
            attr_name: 要添加的子屬性名。
            parent_attr_name: 父屬性名。
            obj_name: 對象的名稱。

        範例:
            YourClass.add_string_child_attr("childAttr", "parentAttr", "objName")

        返回:
            無。
        """
        nice_name = (
            attr_name.replace(parent_attr_name, "")
            if parent_attr_name in attr_name
            else attr_name
        )
        cmds.addAttr(
            obj_name,
            longName=attr_name,
            niceName=nice_name,
            dataType="string",
            parent=parent_attr_name,
        )

    @classmethod
    def set_string_attr(cls, attr_name, attr_value, obj_name):
        """
        設定指定對象的單個字符串屬性。

        參數:
            attr_name: 要設定的屬性名。
            attr_value: 要設定的屬性值。如果為 None，將設為空字符串。
            obj_name: 對象的名稱。

        範例:
            YourClass.set_string_attr("attributeName", "value", "objName")

        返回:
            無。
        """
        if attr_value is None:
            attr_value = ""
        cmds.setAttr(f"{obj_name}.{attr_name}", attr_value, type="string")

    @classmethod
    def set_attr(cls, obj_name, attr_name, attr_value):
        cmds.setAttr(f"{obj_name}.{attr_name}", attr_value)

    @classmethod
    def add_string_attr_to_obj(cls, attr_compound_name, attrs, obj_name):
        """
        向指定的對象添加一個字符串屬性。

        參數:
            attr_compound_name: 要添加的屬性的名稱。
            attrs: 字典，其中包含要添加的屬性和相應的值。
            obj_name: 對象的名稱。

        範例:
            YourClass.add_string_attr_to_obj("newAttr", {"childAttr": "value"}, "objName")

        返回:
            無。
        """
        if not cls.obj_exists(obj_name):
            helper.Logger.warning(__name__, f"{obj_name} Object does not exist.")
            return

        if not cls.attr_exists(attr_compound_name, obj_name):
            cls.add_compound_attr(attr_compound_name, len(attrs), obj_name)
        else:
            helper.Logger.warning(__name__, f"{attr_compound_name} attribute exists")

        for add_attr, _ in attrs.items():
            if not cls.attr_exists(add_attr, obj_name):
                cls.add_string_child_attr(add_attr, attr_compound_name, obj_name)
            else:
                helper.Logger.warning(__name__, f"{add_attr} attribute exists")

    @classmethod
    def set_string_attr_to_obj(cls, attr_compound_name, attrs, obj_name):
        """
        設定指定對象上的一個或多個字符串屬性的值。

        參數:
            attr_compound_name: 要設定的複合屬性的名稱。
            attrs: 字典，其中包含要設定的屬性和相應的值。
            obj_name: 對象的名稱。

        範例:
            YourClass.set_string_attr_to_obj("existingAttr", {"childAttr": "new_value"}, "objName")

        返回:
            無。
        """
        if not cls.obj_exists(obj_name):
            helper.Logger.warning(__name__, f"{obj_name} Object does not exist.")
            return
        if not cls.attr_exists(attr_compound_name, obj_name):
            cls.add_compound_attr(attr_compound_name, len(attrs), obj_name)
        else:
            helper.Logger.warning(__name__, f"{attr_compound_name} attribute exists")

        for set_attr, set_value in attrs.items():
            if cls.attr_exists(set_attr, obj_name):
                cls.set_string_attr(set_attr, set_value, obj_name)
            else:
                helper.Logger.warning(__name__, f"{set_attr} attribute exists")

    @classmethod
    def setup_string_attr_to_obj(cls, prefix, attrs, obj_name):
        """
        為指定物件設置多個字符串屬性。

        參數:
            prefix: 屬性名稱前綴。
            attrs: 要添加和設置的屬性名稱列表。
            obj_name: 目標物件名稱。

        範例:
            YourClass.setup_string_attr_to_object("prefix_", ["attr1", "attr2"], "my_object")

        返回:
            無。
        """
        cls.add_string_attr_to_obj(prefix, attrs, obj_name)
        cls.set_string_attr_to_obj(prefix, attrs, obj_name)

    @classmethod
    def add_group(cls, obj_name):
        """
        在Maya場景中添加一個空的組。

        參數:
            obj_name: str
                期望創建的組名稱。

        範例:
            group = YourClass.add_group("my_new_group")  # 創建名為 "my_new_group" 的組

        返回:
            創建的組的名稱。
        """
        if cls.obj_exists(obj_name):
            helper.Logger.warning(__name__, f"{obj_name} Object already exists.")
            return obj_name
        return cmds.group(empty=True, name=obj_name)

    @classmethod
    def add_locator(cls, obj_name):
        """
        在Maya場景中添加一個定位器。

        參數:
            obj_name: str
                期望創建的定位器名稱。

        範例:
            locator = YourClass.add_locator("my_new_locator")  # 創建名為 "my_new_locator" 的定位器

        返回:
            創建的定位器的名稱。
        """
        if cls.obj_exists(obj_name):
            helper.Logger.warning(__name__, f"{obj_name} Object already exists.")
            return obj_name
        return cmds.spaceLocator(name=obj_name)

    @classmethod
    def get_compound_attrs(cls, obj_name):
        attr = cmds.listAttr(obj_name, userDefined=True, write=True) or []
        tags = [
            at
            for at in attr
            if cmds.attributeQuery(at, node=obj_name, numberOfChildren=True) is not None
        ]
        return tags

    @classmethod
    def get_attrs(cls, obj_name):
        """
        獲取指定對象的所有屬性。

        參數:
            obj_name: 要獲取屬性的對象的名稱。

        範例:
            attrs = YourClass.get_attrs("objName")

        返回:
            包含所有屬性名稱的列表。
        """
        # TODO: 需重構
        all_attrs = {}
        user_attrs = cmds.listAttr(obj_name, userDefined=True, write=True) or []

        for attr in user_attrs:
            if cmds.attributeQuery(attr, node=obj_name, numberOfChildren=True):
                attr_dict = {}
                ch_attrs = (
                    cmds.attributeQuery(attr, node=obj_name, listChildren=True) or []
                )

                for ch in ch_attrs:
                    val = cmds.getAttr(f"{obj_name}.{ch}")
                    if val is not None:
                        key = ch.replace("_", "")
                        attr_dict[key] = str(val) if isinstance(val, float) else val

                all_attrs[attr] = attr_dict
            elif not any(attr in sub_attr_dict for sub_attr_dict in all_attrs.values()):
                val = cmds.getAttr(f"{obj_name}.{attr}")
                if val is not None:
                    key = attr.replace("_", "")
                    all_attrs[key] = str(val) if isinstance(val, float) else val
        return all_attrs

    @classmethod
    def select(cls, obj_name):
        """
        選擇Maya場景中的指定對象。

        參數:
            obj_name: 要選擇的對象的名稱。

        範例:
            YourClass.select("objName")

        返回:
            無。
        """
        cmds.select(obj_name, replace=True)

    @classmethod
    def parent(cls, obj_name, parent_obj_name):
        """
        獲取Maya場景中選擇對象的父對象。

        範例:
            parent = YourClass.parent()

        返回:
            父對象的名稱。
        """
        cmds.parent(obj_name, parent_obj_name)

    @classmethod
    def delete(cls, obj_name):
        """
        從Maya場景中刪除指定的對象。

        參數:
            obj_name: 要刪除的對象的名稱。

        範例:
            YourClass.remove("objName")

        返回:
            無。
        """
        cmds.delete(obj_name)
