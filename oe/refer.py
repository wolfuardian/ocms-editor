class Corp:
    NADI = "NADI"

class Product:
    ID = "ocms-editor"

class Registry:
    REG_KEY = f"Software\\{Corp.NADI}"
    REG_SUB = f"{Product.ID}"

    REG_PROJ_DIR = "Pref_ProjectDirectory"
    REG_RES_DIR = "Pref_ResourcesDirectory"
    REG_XML_PATH = "Pref_XmlPath"

    REG_XML_DOC = "Pref_XmlDocument"

class IO:
    SIZE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]

class Qt:
    ICON_DIR = "/oe/utils/resources/"
