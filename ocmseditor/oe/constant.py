import os
import re
from enum import Enum
from pathlib import Path

LOGGER_NAME = "ocmseditor"


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
# PATH
#
MODULE_FOLDER_PATH = os.path.dirname(os.path.dirname(__file__))
ICON_FOLDER_PATH = "/data/icons/"


#
# STRING
#
INVALID_CHARS_PATTERN = re.compile(r"[^a-zA-Z0-9_]")


#
# INFO
#
INFO__NOT_YET_RESOLVED = "<Not yet resolved>"
INFO__RESOLVED_FAILED = "<Resolved failed>"
