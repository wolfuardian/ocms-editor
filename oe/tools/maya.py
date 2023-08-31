import re
import sys
import maya.OpenMayaUI as omui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import oe.core.tools as core
import oe.tools as tools


class Maya(core.Maya):
    @classmethod
    def get_main_window(cls):
        maya_main_ptr = omui.MQtUtil.mainWindow()
        if sys.version_info.major >= 3:
            return wrapInstance(int(maya_main_ptr), QtWidgets.QWidget)
        else:
            return wrapInstance(long(maya_main_ptr), QtWidgets.QWidget)

    @classmethod
    def decode_utf8_string(cls, byte_string):
        try:
            decoded_string = byte_string.decode("utf-8")
            return decoded_string
        except UnicodeDecodeError:
            # print(f"Decode error: {byte_string}, clip last byte and try again.")
            new_byte_string = byte_string[:-1]
            return cls.decode_utf8_string(new_byte_string)

    @classmethod
    def decode_fbxasc_string(cls, fbxasc_string):
        if "FBXASC" not in fbxasc_string:
            return fbxasc_string
        prefix = "FBXASC"
        decoded_string = fbxasc_string
        matches = re.findall(f'{prefix}\d{{3}}', fbxasc_string)

        for match in matches:
            decoded_char = chr(int(match[len(prefix):]))
            decoded_string = decoded_string.replace(match, decoded_char)

        byte_string = decoded_string.encode("iso-8859-1")
        return cls.decode_utf8_string(byte_string)
