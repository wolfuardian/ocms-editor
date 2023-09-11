# -*- coding: utf-8 -*-

import os
import sys
import shutil
import getpass
import logging
import zipfile
import textwrap
import importlib

import pymel.core as pm
import maya.mel as mel
import maya.cmds as cmds
import maya.OpenMayaUI as omui

from PySide2 import QtWidgets, QtGui, QtCore
from shiboken2 import wrapInstance


def _hex(h):
    return "#" + h


DEBUG_MODE = True


class TaskSetupMayaModuleFile:
    def __init__(self, task__operate_file):
        self.task__operate_file: TaskOperateFile = task__operate_file
        self.prod_id = self.task__operate_file.prod_id
        self.module_folder_dir = self.task__operate_file.extracted_folder_dir
        self.maya_version = cmds.about(version=True)
        self.maya_modules_dir = ""
        self.maya_mod_file = ""
        self.mod = ""
        self.version = ""
        self.reloaded_modules = None

    def func__reload_module(self, module_name):
        if self.module_folder_dir not in sys.path:
            sys.path.append(self.module_folder_dir)

        try:
            if module_name in sys.modules:
                module = importlib.reload(sys.modules[module_name])
            else:
                module = importlib.import_module(module_name)
        finally:
            pass

        return module

    def task__reload_modules(self):
        self.reloaded_modules = [
            self.func__reload_module("oe"),
            self.func__reload_module("product"),
        ]

    def task__setup_maya_shelf(self):
        maya_shelf = self.mod.replace("-", "_")

        if not cmds.layout(maya_shelf, exists=True):
            logging.getLogger("Maya").info(f"Creating {maya_shelf} shelf tab")
            c = 'addNewShelfTab("' + maya_shelf + '");'
            mel.eval(c)

        icon_path = "/execute.png"

        command = textwrap.dedent(
            """\
            from ocmseditor import win
            win.show()"""
        )

        shelf_mbim = cmds.shelfLayout(maya_shelf, query=True, childArray=True)
        if shelf_mbim:
            logging.getLogger("Maya").info(f"Clearing {maya_shelf} shelf buttons")
            for button in shelf_mbim:
                cmds.deleteUI(button, control=True)

        cmds.shelfButton(
            annotation="Run",
            image1=icon_path,
            command=command,
            parent=maya_shelf,
            label="run",
        )

    def task__setup_maya_module(self):
        self.maya_modules_dir = os.path.join(
            os.getenv("MAYA_APP_DIR"), self.maya_version, "modules"
        )
        self.maya_mod_file = os.path.join(self.maya_modules_dir, "ocms-editor.mod")
        if os.path.exists(self.maya_mod_file):
            os.remove(self.maya_mod_file)

        self.mod = self.prod_id.split("-")[0] + "-" + self.prod_id.split("-")[1]
        self.version = self.prod_id.split("-")[2]
        self.module_folder_dir = self.module_folder_dir.replace("\\", "/")

        if DEBUG_MODE:
            env_dir = f"C:/Users/{getpass.getuser()}/PycharmProjects"
            ver = "ocms-editor-2308-0024"
            mod = ver.split("-")[0] + "-" + ver.split("-")[1]
            mod_ver = ver.split("-")[2]
            mod_dir = f"{env_dir}/{mod}"

            with open(self.maya_mod_file, "w") as f:
                f.write(f"+ {mod} {mod_ver} {mod_dir}\n")
                f.write(f"scripts: {mod_dir}")
        else:
            with open(self.maya_mod_file, "w") as f:
                f.write(f"+ {self.mod} {self.version} {self.module_folder_dir}\n")
                f.write(f"scripts: {self.module_folder_dir}\n")

    def execute_tasks(self):
        self.task__setup_maya_module()

        self.task__setup_maya_shelf()

        self.task__reload_modules()


class TaskOperateFile:
    def __init__(self, zip_filepath, prod_id):
        self.zip_filepath = zip_filepath
        self.prod_id = prod_id
        self.module_dir = ""
        self.extracted_folder_dir = ""

    @staticmethod
    def func__rename_zip_file(source, destination):
        if os.path.exists(destination):
            os.remove(destination)
        os.rename(source, destination)

    def func__get_correct_filename(self):
        filename_ext = os.path.basename(self.zip_filepath)
        filename, _ = os.path.splitext(filename_ext)
        if filename != self.prod_id:
            new_filename = self.prod_id + ".zip"
            new_filepath = os.path.join(
                os.path.dirname(self.zip_filepath), new_filename
            )
            return new_filepath
        return self.zip_filepath

    @staticmethod
    def func__get_module_path():
        return os.path.join(
            os.path.expanduser("~"),
            "Documents",
            "ocms_editor",
            f"py{sys.version_info.major}",
        )

    def task__cleanup_zip_file(self):
        os.remove(self.zip_filepath)

    def task__unpack_zip(self):
        filename, _ = os.path.splitext(self.zip_filepath)
        self.extracted_folder_dir = os.path.join(
            os.path.dirname(self.zip_filepath), filename
        )
        if os.path.exists(self.extracted_folder_dir):
            shutil.rmtree(self.extracted_folder_dir)
        with zipfile.ZipFile(self.zip_filepath, "r") as zip_ref:
            zip_ref.extractall(os.path.dirname(self.zip_filepath))

    def task__move_zip_to_module_dir(self):
        new_filepath = self.func__get_correct_filename()
        if DEBUG_MODE:
            shutil.copy2(self.zip_filepath, new_filepath)
        else:
            shutil.move(self.zip_filepath, new_filepath)
        self.zip_filepath = new_filepath

    def task__create_module_dir(self):
        self.module_dir = self.func__get_module_path()
        if not os.path.exists(self.module_dir):
            os.makedirs(self.module_dir)

    def execute_tasks(self):
        self.task__create_module_dir()

        self.task__move_zip_to_module_dir()

        self.task__unpack_zip()

        self.task__cleanup_zip_file()


class TaskBrowseZip:
    def __init__(self):
        self.zip_filepath = ""
        self.prod_id = ""

    @staticmethod
    def func__check_empty_or_not_found(prod_id):
        if prod_id == "" or not prod_id:
            raise ValueError("Product ID is empty.")

    @staticmethod
    def func__check_product_ocms_editor(prod_id):
        if not prod_id.startswith("ocms-editor"):
            raise ValueError("Product ID does not start with 'ocms-editor'")

    @staticmethod
    def func__check_product_id_format(prod_id, separator, expected_count):
        if len(prod_id.split(separator)) != expected_count:
            raise ValueError("Product ID format is incorrect.")

    @staticmethod
    def func__check_version_format(version):
        segments = version.split(".")
        if len(segments) != 3:
            raise ValueError("Product version format is incorrect.")
        if len(segments[0]) != 1 or len(segments[1]) != 4 or len(segments[2]) != 4:
            raise ValueError("Product version format is incorrect.")

    @staticmethod
    def func__parse_prod_id_from_line(line):
        if line.startswith("prod_id"):
            return line.split('"')[1]
        raise ValueError("There is no product id in the product file.")

    @staticmethod
    def func__read_first_line_from_zip_namelist(zip_path, version_file):
        import zipfile

        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                with zip_ref.open(zip_ref.namelist()[0] + version_file) as f:
                    return f.readline().decode("utf-8").strip()
        except KeyError:
            raise ValueError("Product file not found in zip file.")

    def func__validate_prod_id(self, prod_id):
        self.func__check_empty_or_not_found(prod_id)
        self.func__check_product_ocms_editor(prod_id)
        self.func__check_product_id_format(prod_id, "-", 3)
        self.func__check_version_format(prod_id.split("-")[-1])

    def func__get_prod_id_from_zip(self, zip_path, version_file):
        first_line = self.func__read_first_line_from_zip_namelist(
            zip_path, version_file
        )
        return self.func__parse_prod_id_from_line(first_line)

    def func__check_zip_validity(self, filepath):
        self.prod_id = self.func__get_prod_id_from_zip(filepath, "product.py")
        self.func__validate_prod_id(self.prod_id)

    @staticmethod
    def func__select_zip_file(start_dir=None, file_filter="Zip (*.zip)"):
        start_dir = start_dir or os.path.join(
            os.path.expanduser("~"), "Documents", "maya"
        )
        filepath = pm.fileDialog2(fileMode=1, dir=start_dir, fileFilter=file_filter)
        if not filepath:
            raise FileNotFoundError("User cancelled the file selection.")
        return filepath[0]

    def func__get_valid_zip_filepath(self, start_dir=None, file_filter="Zip (*.zip)"):
        filepath = self.func__select_zip_file(start_dir, file_filter)
        self.func__check_zip_validity(filepath)
        return filepath

    def task__set_zip_filepath(self):
        self.zip_filepath = self.func__get_valid_zip_filepath()

    def execute_tasks(self):
        self.task__set_zip_filepath()


class InstallData:
    def __init__(self):
        self.maya_version = cmds.about(version=True)
        self.zip_filepath = ""
        self.prod_id = ""

    def op__browse_zip(self, parent):
        task__browse_zip = TaskBrowseZip()
        task__browse_zip.execute_tasks()
        self.zip_filepath = task__browse_zip.zip_filepath
        self.prod_id = task__browse_zip.prod_id
        parent.browse_zip_lbl.setText(self.zip_filepath)
        parent.browse_zip_lbl.setStyleSheet(f'color: {_hex("81c784")}')
        parent.install_btn.setEnabled(True)

    def op__install(self, parent):
        task__operate_file = TaskOperateFile(self.zip_filepath, self.prod_id)
        task__operate_file.execute_tasks()

        task__setup_maya_module_file = TaskSetupMayaModuleFile(task__operate_file)
        task__setup_maya_module_file.execute_tasks()

        parent.install_btn.setEnabled(False)

        parent.deleteLater()


class InstallWindow(QtWidgets.QDialog):
    def __init__(self, data, parent=None):
        super(InstallWindow, self).__init__(parent)
        self.data: InstallData = data

        self.setWindowTitle("Install Wizard")
        self.resize(320, 130)
        self.setModal(True)

        self.func__center_window()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setContentsMargins(0, 24, 0, 24)
        layout.setSpacing(24)

        version_vbl = QtWidgets.QVBoxLayout()
        version_vbl.setContentsMargins(0, 0, 0, 0)
        version_vbl.setSpacing(0)

        self.version_lbl = QtWidgets.QLabel("Maya Version: " + cmds.about(version=True))
        self.version_lbl.setAlignment(QtCore.Qt.AlignHCenter)
        self.version_lbl.setFont(QtGui.QFont("Arial", 8))
        version_vbl.addWidget(self.version_lbl)

        layout.addWidget(self.version_lbl)

        zip_vbl = QtWidgets.QVBoxLayout()
        zip_vbl.setContentsMargins(0, 0, 0, 0)
        zip_vbl.setSpacing(0)

        self.browse_zip_lbl = QtWidgets.QLabel("uninitialized")
        self.browse_zip_lbl.setAlignment(QtCore.Qt.AlignHCenter)
        self.browse_zip_lbl.setFont(QtGui.QFont("Arial", 8))
        self.browse_zip_lbl.setStyleSheet(f'color: {_hex("fd8a6a")}')
        zip_vbl.addWidget(self.browse_zip_lbl)
        layout.addLayout(zip_vbl)

        self.browse_zip_btn = QtWidgets.QPushButton("Browse Zip")
        self.browse_zip_btn.clicked.connect(lambda: self.data.op__browse_zip(self))
        self.browse_zip_btn.setFixedHeight(16)
        zip_vbl.addWidget(self.browse_zip_btn)

        self.download_from_github = QtWidgets.QPushButton("Download from GitHub")
        self.download_from_github.setFixedHeight(16)
        self.download_from_github.setEnabled(False)
        zip_vbl.addWidget(self.download_from_github)

        install_vbl = QtWidgets.QVBoxLayout()
        install_vbl.setContentsMargins(0, 0, 0, 0)
        install_vbl.setSpacing(0)

        self.install_btn = QtWidgets.QPushButton("Install")
        self.install_btn.setFixedHeight(48)
        self.install_btn.clicked.connect(lambda: self.data.op__install(self))
        self.install_btn.setEnabled(False)
        install_vbl.addWidget(self.install_btn)
        layout.addLayout(install_vbl)

        uninstall_vbl = QtWidgets.QVBoxLayout()
        uninstall_vbl.setContentsMargins(0, 0, 0, 0)
        uninstall_vbl.setSpacing(0)

        self.uninstall_btn = QtWidgets.QPushButton("Uninstall")
        self.uninstall_btn.setFixedHeight(48)
        self.uninstall_btn.setEnabled(False)

        uninstall_vbl.addWidget(self.uninstall_btn)
        layout.addLayout(uninstall_vbl)

    def func__center_window(self):
        parent = self.func__get_maya_main_window()
        if parent is None:
            return

        parent_geo = parent.frameGeometry()
        self_geo = self.frameGeometry()
        center_point = parent_geo.center()

        self_geo.moveCenter(center_point)
        self.move(self_geo.topLeft())

    @staticmethod
    def func__get_maya_main_window():
        maya_main_ptr = omui.MQtUtil.mainWindow()
        # noinspection PyUnresolvedReferences
        ptr_type = int if sys.version_info.major >= 3 else long
        return wrapInstance(ptr_type(maya_main_ptr), QtWidgets.QWidget)


def main():
    if sys.version_info.major == 2:
        raise Exception("This script is only compatible with Python 3.")

    data = InstallData()
    win = InstallWindow(data)
    win.exec_()


# noinspection PyPep8Naming
def onMayaDroppedPythonFile():
    main()


if __name__ == "__main__":
    main()
