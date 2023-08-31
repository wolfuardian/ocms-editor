class Corp:
    NADI = "NADI"

class Product:
    ID = "ocms-editor"

class Registry:
    REG_KEY = f"Software\\{Corp.NADI}"
    REG_SUB = f"{Product.ID}"
    REG_PROJECT_DIRECTORY = "Project_Directory"
    REG_RESOURCES_SOURCE_DIRECTORY = "Resources_Source_Directory"
    REG_RESOURCES_TARGET_DIRECTORY = "Resources_Target_Directory"
    REG_XML_DIRECTORY = "XML_Directory"
    REG_XML_STRING = "XML_String"

class Qt:
    RES_DIR = "/oe/utils/resources/"
