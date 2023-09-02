import io

import oe.tools as tools
import oe.core.tools as core

class IO(core.IO):
    @classmethod
    def read_utf16(cls, path):
        return io.open(path, mode="r", encoding="utf-16").read()
