import ocmseditor.tool as tool
import ocmseditor.oe.helper as helper
import ocmseditor.oe.data.const as const


def op_fetch_xml_filepath(self):
    helper.Logger.info(__name__, "Fetching xml filepath")
    # Operator: Fetch -> Validate
    self._validate()


def op_browser_xml_filepath(self):
    helper.Logger.info(__name__, "Browsing xml filepath")
    # Operator: Browser -> Validate
    default_dir = tool.Registry.get_reg(const.REG_XML_FILEPATH)
    filepath = tool.Maya.browser(1, default_dir, "All Files (*.*)")
    if not filepath:
        return
    tool.Registry.set_reg(const.REG_XML_FILEPATH, filepath)
    self._validate()


def op_parse_xml(self):
    helper.Logger.info(__name__, "Parsing xml")
    # Operator: Browser -> Validate -> Parse
    parse_xml(self)


def op_write_ocms_datasheet(self, *args):
    helper.Logger.info(__name__, "Starting to write OCMS Datasheet")
    # Operator: Browser -> Validate -> Parse -> Write Datasheet
    default_path = tool.Registry.get_reg(const.REG_PROJ_PATH)
    folder_path = tool.Maya.browser(3, default_path, "All Folders (*.*)")
    if not folder_path:
        return
    ocms = tool.OCMS.get_ocms()
    parse_filepath = folder_path + "\\" + "output_xml_parse_data.log"
    collect_filepath = folder_path + "\\" + "output_xml_collect_data.log"

    ocms.write_datasheet(parse_filepath, ocms.xml.parse_data, *args)
    ocms.write_datasheet(collect_filepath, ocms.xml.collect_data, *args)

    tool.File.open_on_explorer(collect_filepath)

    helper.Logger.info(__name__, "Finished writing OCMS Datasheet")


def parse_xml(self):
    helper.Logger.info(__name__, "Starting to parse xml")
    # Operator: Browser -> Validate -> Parse

    xml_path = tool.Registry.get_reg(const.REG_XML_FILEPATH)

    ocms = tool.OCMS.get_ocms()
    ocms.xml.load(path=xml_path)
    ocms.xml.done()

    self._destroy()
    self.parsed = True
    self._construct()
    helper.Logger.info(__name__, "Finished parsing xml")
