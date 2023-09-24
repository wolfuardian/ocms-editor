import ocmseditor.tool as tool
import ocmseditor.oe.helper as helper
import ocmseditor.oe.data.const as const


def op_fetch_resource_path(self):
    helper.Logger.info(__name__, "Fetching resource path")
    # Operator: Fetch -> Validate
    self._validate()


def op_browser_resource_path(self):
    helper.Logger.info(__name__, "Browsing resource path")
    # Operator: Browser -> Validate
    default_path = tool.Registry.get_reg(const.REG_RES_PATH)
    folder_path = tool.Maya.browser(3, default_path, "All Folders (*.*)")
    if not folder_path:
        return
    tool.Registry.set_reg(const.REG_RES_PATH, folder_path)
    self._validate()


def op_parse(self):
    helper.Logger.info(__name__, "Parsing resource")
    # Operator: Browser -> Validate -> Parse
    parse_resource(self)


def op_import_resource(self):
    helper.Logger.info(__name__, "Importing resource")
    # Operator: Browser -> Validate -> Parse -> Import
    import_resource(self)


def op_write_datasheet(self, *args):
    helper.Logger.info(__name__, "Starting to write OCMS Datasheet")
    # Operator: Browser -> Validate -> Parse -> Write Datasheet
    default_path = tool.Registry.get_reg(const.REG_PROJ_PATH)
    folder_path = tool.Maya.browser(3, default_path, "All Folders (*.*)")
    if not folder_path:
        return
    ocms = tool.OCMS.get_ocms()
    parse_filepath = folder_path + "\\" + "output_res_parse_data.log"
    collect_filepath = folder_path + "\\" + "output_res_collect_data.log"

    ocms.write_datasheet(parse_filepath, ocms.res.parse_data, *args)
    ocms.write_datasheet(collect_filepath, ocms.res.collect_data, *args)

    tool.File.open_on_explorer(collect_filepath)

    helper.Logger.info(__name__, "Finished writing OCMS Datasheet")


def parse_resource(self):
    helper.Logger.info(__name__, "Starting to parse resource")
    # Operator: Browser -> Validate -> Parse

    res_path = tool.Registry.get_reg(const.REG_RES_PATH)

    ocms = tool.OCMS.get_ocms()
    ocms.res.load(path=res_path)
    ocms.res.done()

    self._destroy()
    self.parsed = True
    self._construct()
    helper.Logger.info(__name__, "Finished parsing resource")


def import_resource(self):
    helper.Logger.info(__name__, "Importing resource")

    model_importer = helper.ModelImporter()
    model_importer.execute()

    ocms_sync_handler = helper.OCMSDataSyncHandler()
    ocms_sync_handler.execute()

    helper.Logger.info(__name__, "Finished importing resource")
