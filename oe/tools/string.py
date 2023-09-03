from typing import List, Any, Dict

import oe.tools as tools
import oe.core.tools as core


class String(core.String):
    @classmethod
    def list_to_string(cls, lst: List[Any]) -> str:
        return ", ".join(map(str, lst)) if lst else ""

    @classmethod
    def dict_to_string(cls, dictionary: Dict[Any, Any]) -> str:
        return (
            ", ".join(f"{key}: {value}" for key, value in dictionary.items())
            if dictionary
            else ""
        )
