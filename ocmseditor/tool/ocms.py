import ocmseditor.core.tool as core

from ocmseditor.oe.ocms import OCMSStore


class OCMS(core.OCMS):
    @classmethod
    def get_ocms(cls):
        """
        獲取 OCMSStore 的實例。

        範例:
            store = YourClass.get_ocms()

        返回:
            OCMSStore 的實例。
        """
        return OCMSStore()
