import re

import ocmseditor.core.tool as core


class Name(core.Name):
    @classmethod
    def to_underscore(cls, name):
        """
        將輸入的字符串中的非字母數字字符替換為下劃線。

        參數:
            name: 輸入的字符串。

        範例:
            result = YourClass.to_underscore("Hello World!")  # 返回 "Hello_World_"

        返回:
            經過替換後的字符串。
        """
        # return re.sub(r"\W+", "_", name)
        return re.sub(r"(\W+)", lambda m: "_" * len(m.group(1)), name)
