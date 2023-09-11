from typing import List, Any, Dict

import ocmseditor.core.tool as core

from ocmseditor import tool


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

    @classmethod
    def wrap_text(cls, text, left="<", right=">"):
        return f"{left}{text}{right}"
