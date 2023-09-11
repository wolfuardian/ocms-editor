import ocmseditor.core.tool as core

from ocmseditor import tool
from ocmseditor.oe import ocms

class UI(core.UI):
    @classmethod
    def update(cls):
        tool.Log.info(__name__, "Updating UI")

        from ocmseditor.oe.module.setproject import operator as setproject_operator
        from ocmseditor.oe.module.parsexml import operator as parsexml_operator
        from ocmseditor.oe.module.parseres import operator as parseres_operator

        _ui = ocms.UIStore.ui.get("frame_set_project")
        setproject_operator.op_fetch(_ui)

        _ui = ocms.UIStore.ui.get("frame_parse_xml")
        parsexml_operator.op_fetch(_ui)

        _ui = ocms.UIStore.ui.get("frame_parse_res")
        parseres_operator.op_fetch_res_dir(_ui)


