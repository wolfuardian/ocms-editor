# -*- coding: utf-8 -*-
import hashlib
import importlib
import logging
import os
import shutil
import sys

import pymel.core as pm
import maya.mel as mel
import maya.cmds as cmds
import maya.OpenMayaUI as omui

from PySide2 import QtWidgets, QtGui, QtCore
from shiboken2 import wrapInstance


def _hex(h):
    return "#" + h


def get_maya_main_window():
    maya_main_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(maya_main_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(maya_main_ptr), QtWidgets.QWidget)


class InstallData:
    def __init__(self):
        self.maya_version = cmds.about(version=True)
        self.zip_filepath = ""
        self.prod_id = ""
        self.is_zip_available = False

    def browse_zip(self, win):
        win: InstallWindow
        self.zip_filepath = self.get_zip_filepath()
        if self.zip_filepath == "Cancel":
            logging.getLogger("Operator").info("User canceled the browser dialog.")
            return
        if self.zip_filepath == "NotValid":
            logging.getLogger("Operator").info("User selected an invalid zip file.")
            win.browse_zip_lbl.setText("Invalid zip file!")
            win.browse_zip_lbl.setStyleSheet(f'color: {_hex("fd8a6a")}')
            self.is_zip_available = False
            win.update_gui()
            return
        win.browse_zip_lbl.setText(self.zip_filepath + "\nZip file is available.")
        win.browse_zip_lbl.setStyleSheet(f'color: {_hex("81c784")}')
        self.is_zip_available = True
        logging.getLogger("Operator").info("Zip file is available.")
        win.update_gui()

    def install(self, win):
        win: InstallWindow
        win.browse_zip_lbl.setText("Installing...")
        logging.getLogger("Operator").info("Installing...")
        QtWidgets.QApplication.processEvents()

        if not self.is_zip_standby_in_dest(
            self.move_zip_to_dest(
                self.get_correct_zip_filename(self.zip_filepath, self.prod_id)
            )
        ):
            logging.getLogger("Operator").error(
                "Zip file is not standby in destination."
            )
            win.browse_zip_lbl.setText(
                "Zip file is not standby in destination! Please try again."
            )
            win.browse_zip_lbl.setStyleSheet(f'color: {_hex("fd8a6a")}')
            return "UnknownError"

        win.browse_zip_lbl.setText(self.zip_filepath + "\nZip file is standby.")
        win.browse_zip_lbl.setStyleSheet(f'color: {_hex("81c784")}')
        logging.getLogger("Operator").info(f"Zip file {self.zip_filepath} is standby.")
        QtWidgets.QApplication.processEvents()

        extracted_folder = self.unpack_zip(self.zip_filepath)
        self.cleanup_zip_file(self.zip_filepath)
        modules_dir = os.path.join(
            os.getenv("MAYA_APP_DIR"), self.maya_version, "modules"
        )
        if not os.path.exists(modules_dir):
            os.makedirs(modules_dir)
        mod_file = os.path.join(modules_dir, "ocms-editor.mod")
        if os.path.exists(mod_file):
            logging.getLogger("FileIO").warning(
                "Module file already exists in the destination. Cleaning existing file..."
            )
            os.remove(mod_file)
        extracted_folder = extracted_folder.replace("\\", "/")
        mod = self.prod_id.split("-")[0] + "-" + self.prod_id.split("-")[1]
        mode_version = self.prod_id.split("-")[2]
        with open(mod_file, "w") as f:
            f.write(f"+ {mod} {mode_version} {extracted_folder}\n")
            f.write(f"scripts: {extracted_folder}\n")
        logging.getLogger("FileIO").info("Creating module file... Done!")

        maya_shelf = mod.replace("-", "_")

        if not cmds.layout(maya_shelf, exists=True):
            logging.getLogger("Maya").info(f"Creating {maya_shelf} shelf tab")
            c = 'addNewShelfTab("' + maya_shelf + '");'
            mel.eval(c)

        import textwrap
        
        command = textwrap.dedent(
            """\
            from oe import gui
            gui.show()"""
        )

        icon_path = "/execute.png"

        shelf_mbim = cmds.shelfLayout(maya_shelf, query=True, childArray=True)
        if shelf_mbim:
            logging.getLogger("Maya").info(f"Clearing {maya_shelf} shelf buttons")
            for button in shelf_mbim:
                cmds.deleteUI(button, control=True)

        logging.getLogger("Maya").info(f"Creating {maya_shelf} shelf button")
        cmds.shelfButton(
            annotation="Run",
            image1=icon_path,
            command=command,
            parent=maya_shelf,
            label="run",
        )

        reloaded_modules = [
            reload_module_by_path("oe", extracted_folder),
            reload_module_by_path("product", extracted_folder),
        ]
        logging.getLogger("PyModule").info(f"Reloaded module: {reloaded_modules}")
        logging.getLogger("Operator").info("Installation complete!")

        win.install_btn.setEnabled(False)

    @staticmethod
    def is_zip_standby_in_dest(zip_dest):
        if os.path.exists(zip_dest):
            return True
        return False

    def get_correct_zip_filename(self, filepath, prod_id):
        filename_ext = os.path.basename(filepath)
        filename, _ = os.path.splitext(filename_ext)
        if filename != prod_id:
            logging.getLogger("FileIO").warning(
                "Zip file name is not correct. Renaming..."
            )
            new_filename = prod_id + ".zip"
            new_filepath = os.path.join(os.path.dirname(filepath), new_filename)
            self.rename_zip_file(filepath, new_filepath)
            self.zip_filepath = new_filepath
            return new_filepath
        return filepath

    @staticmethod
    def rename_zip_file(source, dest):
        if os.path.exists(dest):
            logging.getLogger("FileIO").warning(
                "Zip file already exists in the destination. Cleaning existing file..."
            )
            os.remove(dest)
        logging.getLogger("FileIO").info("Renaming zip file...")
        os.rename(source, dest)

    @staticmethod
    def unpack_zip(filepath):
        # if folder already exists, clean it
        filename, _ = os.path.splitext(filepath)
        extracted_folder = os.path.join(os.path.dirname(filepath), filename)
        if os.path.exists(extracted_folder):
            logging.getLogger("FileIO").warning(
                "Extracted folder already exists in the destination. Cleaning existing folder..."
            )
            shutil.rmtree(extracted_folder)
        import zipfile

        logging.getLogger("FileIO").info("Unzipping...")
        with zipfile.ZipFile(filepath, "r") as zip_ref:
            zip_ref.extractall(os.path.dirname(filepath))
        logging.getLogger("FileIO").info("Unzipping... Done!")
        return extracted_folder

    @staticmethod
    def cleanup_zip_file(zip_filepath):
        logging.getLogger("FileIO").info("Cleaning zip file...")
        os.remove(zip_filepath)
        logging.getLogger("FileIO").info("Cleaning zip file... Done!")

    def move_zip_to_dest(self, filepath):
        mod_dir = os.path.join(
            os.path.expanduser("~"),
            "Documents",
            "ocms_editor",
            f"py{sys.version_info.major}",
        )
        if not os.path.exists(mod_dir):
            os.makedirs(mod_dir)

        zip_dest = os.path.join(mod_dir, os.path.basename(filepath))
        if os.path.exists(zip_dest):
            logging.getLogger("FileIO").warning(
                "File already exists in the destination. Checking file hash..."
            )

            source_hash = self.calculate_file_hash(filepath)
            dest_hash = self.calculate_file_hash(zip_dest)

            if source_hash == dest_hash:
                logging.getLogger("FileIO").warning(
                    "The file is identical. Cleaning and skipping..."
                )
                os.remove(filepath)
                self.zip_filepath = zip_dest
                return zip_dest
            else:
                logging.getLogger("FileIO").warning(
                    "The file is different. Overwriting and cleaning..."
                )
                shutil.copy2(filepath, zip_dest)
                os.remove(filepath)
                self.zip_filepath = zip_dest
                return zip_dest
        logging.getLogger("FileIO").info("Moving zip file to destination...")
        shutil.move(filepath, zip_dest)
        self.zip_filepath = zip_dest
        return zip_dest

    @staticmethod
    def calculate_file_hash(filepath):
        """Calculate the SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def get_zip_filepath(self):
        filepath = pm.fileDialog2(
            fileMode=1,
            dir=os.path.join(os.path.expanduser("~"), "Documents", "maya"),
            fileFilter="Zip (*.zip)",
        )
        if not filepath:
            return "Cancel"
        filepath = filepath[0]
        if not self.is_zip_valid(filepath):
            return "NotValid"
        return filepath

    def is_zip_valid(self, filepath):
        logging.getLogger("FileIO").info("Checking zip file...")
        filename_ext = os.path.basename(filepath)
        filename, _ = os.path.splitext(filename_ext)
        self.prod_id = self.get_prod_id_from_zip(filepath, f"product.py")

        error_code = self.validate_prod_id(self.prod_id)
        if error_code == "ProductIDEmpty":
            logging.getLogger("Product").error(f"Product id is empty.")
            return False
        elif error_code == "ProductNotFound":
            logging.getLogger("Product").error(f"Product file not found in zip file.")
            return False
        elif error_code == "ProductIDHeaderError":
            logging.getLogger("Product").error(
                "product id does not start with 'ocms-editor'"
            )
            return False
        elif error_code == "ProductIDSegmentCountError":
            logging.getLogger("Product").error("product id segment count is not 3")
            return False
        elif error_code == "ProductVersionSegmentCountError":
            logging.getLogger("Product").error("product version segment count is not 3")
            return False
        elif error_code == "ProductVersionMajorNumberError":
            logging.getLogger("Product").error(
                "product version major number does not start with 1 digit"
            )
            return False
        elif error_code == "ProductVersionMinorNumberError":
            logging.getLogger("Product").error(
                "product version minor number does not contain 4 digits"
            )
            return False
        elif error_code == "ProductVersionPatchNumberError":
            logging.getLogger("Product").error(
                "product version patch number does not end with 4 digits"
            )
            return False
        return True

    @staticmethod
    def validate_prod_id(prod_id):
        logging.getLogger("Product").info("Checking product id...")
        if prod_id == "":
            return "ProductIDEmpty"
        if prod_id == "ProductNotFound":
            return "ProductNotFound"
        # Correct product id format: ocms-editor-0.2309.0019
        if not prod_id.startswith("ocms-editor"):
            return "ProductIDHeaderError"
        if not len(prod_id.split("-")) == 3:
            return "ProductIDSegmentCountError"
        version = prod_id.split("-")[-1]
        # Correct version format: 0.2309.0019
        if not len(version.split(".")) == 3:
            return "ProductVersionSegmentCountError"
        if not len(version.split(".")[0]) == 1:
            return "ProductVersionMajorNumberError"
        if not len(version.split(".")[1]) == 4:
            return "ProductVersionMinorNumberError"
        if not len(version.split(".")[2]) == 4:
            return "ProductVersionPatchNumberError"
        return prod_id

    @staticmethod
    def get_prod_id_from_zip(zip_path, version_file):
        extracted_version = None

        import zipfile

        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                with zip_ref.open(zip_ref.namelist()[0] + version_file) as f:
                    first_line = f.readline().decode("utf-8").strip()
                    if first_line.startswith("prod_id"):
                        extracted_version = first_line.split('"')[1]
        except KeyError:
            extracted_version = "ProductNotFound"
        return extracted_version


class InstallWindow(QtWidgets.QDialog):
    def __init__(self, data, parent=None):
        super(InstallWindow, self).__init__(parent)
        self.data = data

        self.setWindowTitle("Install Wizard")
        self.resize(320, 130)
        self.setModal(True)

        self.center_window()

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
        self.browse_zip_btn.clicked.connect(lambda: self.data.browse_zip(self))
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
        self.install_btn.clicked.connect(lambda: self.data.install(self))
        self.install_btn.setEnabled(False)
        install_vbl.addWidget(self.install_btn)
        layout.addLayout(install_vbl)

    def update_gui(self):
        self.install_btn.setEnabled(self.data.is_zip_available)

    def center_window(self):
        parent = get_maya_main_window()
        if parent is None:
            return

        # Get parent window's geometry
        parent_geo = parent.frameGeometry()
        self_geo = self.frameGeometry()

        # Calculate the center point of parent window
        center_point = parent_geo.center()
        self_geo.moveCenter(center_point)

        # Move the window to the center of parent window
        self.move(self_geo.topLeft())


def reload_module_by_path(module_name, module_dir):
    if module_dir not in sys.path:
        sys.path.append(module_dir)

    try:
        if module_name in sys.modules:
            module = importlib.reload(sys.modules[module_name])
        else:
            module = importlib.import_module(module_name)
    finally:
        pass

    return module


def main():
    if sys.version_info.major == 2:
        raise Exception("This script is only compatible with Python 3.")

    data = InstallData()
    win = InstallWindow(data)
    win.exec_()


def onMayaDroppedPythonFile(*args, **kwargs):
    main()


if __name__ == "__main__":
    main()
