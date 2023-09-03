import os
from typing import List, Any

import oe.tools as tools
import oe.core.tools as core


class Dictionary(core.Dictionary):
    @classmethod
    def create_dict_from_lists(cls, keys: List[Any], values: List[Any]) -> dict:
        return dict(zip(keys, values))
