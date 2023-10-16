import os
import re
from enum import Enum
from pathlib import Path

LOGGER_NAME = "ocmseditor"

#
# PATH
#

OCMSEDITOR_ROOT = Path(__file__) / "../.."
VERSION_PATH = OCMSEDITOR_ROOT / "version.txt"
ICON_DIR = OCMSEDITOR_ROOT / "oe" / "utils" / "icons"


class Mode:
    ImportsMode = "Imports Mode"
    FileMode = "File Mode"
    SceneMode = "Scene Mode"


class Fonts:
    Fixedsys = "Fixedsys"
    SegoeUI = "Segoe UI"
    SimSun = "SimSun"
    SimHei = "SimHei"
    MicrosoftYaHei = "Microsoft YaHei"
    MicrosoftJhengHei = "Microsoft JhengHei"
    NSimSun = "NSimSun"
    PMingLiU = "PMingLiU"
    MingLiU = "MingLiU"
    DFKaiSB = "DFKai-SB"
    FangSong = "FangSong"
    KaiTi = "KaiTi"
    FangSong_GB2312 = "FangSong_GB2312"
    KaiTi_GB2312 = "KaiTi_GB2312"
    MSShellDlg2 = "MS Shell Dlg 2"
    HeitiTC = "Heiti TC"


#
# SYSTEM
#

CORP_NAME = "NADI"
PRODUCT_ID = "ocms-editor"

SIZE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]

#
# REGISTRY
#

REG_KEY = f"Software\\{CORP_NAME}"
REG_SUB = f"{PRODUCT_ID}"

REG_PROJ_PATH = "Pref_ProjectPath"
REG_RES_PATH = "Pref_ResourcePath"
REG_XML_FILEPATH = "Pref_XMLFilePath"
REG_XML_EXPORT_FILEPATH = "Pref_XMLExportFilePath"

REG_XML_DOC = "Pref_XMLDocument"

REG_MAYA_JOB_IDS = "Pref_MayaJobIDs"

#
# MODULE
#

NAME_MAPPING = {
    "ocmseditor.oe.helper": "OE.Helper",
    "ocmseditor.oe.ui": "OE.UI",
    "ocmseditor.tool.file": "Tool.File",
    "ocmseditor.tool.maya": "Tool.Maya",
    "ocmseditor.oe.module.setproject.ui": "OE.SetProject.UI",
    "ocmseditor.oe.module.setproject.operator": "OE.SetProject.Operator",
    "ocmseditor.oe.module.parsexml.ui": "OE.ParseXML.UI",
    "ocmseditor.oe.module.parsexml.operator": "OE.ParseXML.Operator",
    "ocmseditor.oe.module.parseres.ui": "OE.ParseResource.UI",
    "ocmseditor.oe.module.parseres.operator": "OE.ParseResource.Operator",
    "ocmseditor.oe.module.toolbox.ui": "OE.ToolBox.UI",
    "ocmseditor.oe.module.toolbox.operator": "OE.ToolBox.Operator",
    "ocmseditor.oe.module.editattr.operator": "OE.EditAttribute.Operator",
}

#
# STRING
#
INVALID_CHARS_PATTERN = re.compile(r"[^a-zA-Z0-9_]")


#
# INFO
#
INFO__NOT_YET_RESOLVED = "<Not yet resolved>"
INFO__RESOLVED_FAILED = "<Resolved failed>"


#
# STATUS
#

INFO__BROWSER_CANCELED = "Browser canceled"
