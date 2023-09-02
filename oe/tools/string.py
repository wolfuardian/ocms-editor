import io

import oe.tools as tools
import oe.core.tools as core

class String(core.String):
    @classmethod
    def join_with_commas(cls, lst):
        result = ', '.join(lst)
        return result
