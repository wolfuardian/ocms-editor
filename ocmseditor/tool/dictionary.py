from typing import List, Any

import ocmseditor.core.tool as core

from ocmseditor import tool


class Dictionary(core.Dictionary):
    @classmethod
    def create_dict_from_lists(cls, keys: List[Any], values: List[Any]) -> dict:
        return dict(zip(keys, values))
