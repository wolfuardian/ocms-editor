import ocmseditor.tool as tool
import ocmseditor.oe.helper as helper
import ocmseditor.oe.data.const as const


def op_fetch_data(self):
    helper.Logger.info(__name__, "Fetching data")
    # Operator: Fetch -> Validate

    ocms = tool.OCMS.get_ocms()
    resource_path = tool.Registry.get_reg(const.REG_RES_PATH)
    if (
        not tool.File.exists(resource_path)
        or not tool.File.is_dir(resource_path)
        or not ocms.xml.valid()
        or not ocms.res.valid()
    ):
        self.import_res = False
    else:
        self.import_res = True

    self._validate()


def op_import_resource(self):
    helper.Logger.info(__name__, "Importing resource")
    # Operator: Browser -> Validate -> Parse -> Import
    import_resource(self)


def import_resource(self):
    helper.Logger.info(__name__, "Importing resource")

    model_importer = helper.ModelImporter()
    model_importer.execute()

    # ocms_sync_handler = helper.OCMSDataSyncHandler()
    # ocms_sync_handler.execute()

    helper.Logger.info(__name__, "Finished importing resource")
