from typing import List, Any, Dict

import oe.module
import oe.tools as tools
import oe.core.tools as core

import oe.storage as storage


class UI(core.UI):
    @classmethod
    def update(cls):
        tools.Log.info(__name__, "Updating UI")

        from oe.module.setproject import operator as setproject_operator
        from oe.module.parsexml import operator as parsexml_operator
        from oe.module.parseres import operator as parseres_operator

        _ui = storage.UIData.ui.get("frame_set_project")
        setproject_operator.op_fetch_project_dir(_ui)

        _ui = storage.UIData.ui.get("frame_parse_xml")
        parsexml_operator.op_fetch_xml_path(_ui)

        _ui = storage.UIData.ui.get("frame_parse_res")
        parseres_operator.op_fetch_res_dir(_ui)
