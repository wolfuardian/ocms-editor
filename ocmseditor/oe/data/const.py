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

REG_PROJ_DIR = "Pref_ProjectDirectory"
REG_RES_DIR = "Pref_ResourcesDirectory"
REG_XML_PATH = "Pref_XMLPath"
REG_XML_EXPORT_PATH = "Pref_XMLExportPath"

REG_XML_DOC = "Pref_XMLDocument"

#
# MODULE
#

NAME_MAPPING = {
    "oe.module.setproject.operator": "SetProject",
    "oe.core.maya": "Maya",
}

#
# PATH
#

ICON_DIR = "/ocmseditor/oe/data/icons/"
