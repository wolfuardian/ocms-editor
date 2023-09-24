import ocmseditor.core.tool as core


class Debug(core.Debug):
    @classmethod
    def print_beautiful_dictionary(cls, data, level, indent):
        """
        遞歸地打印出一個巢狀字典，並以指定的縮進和層級美觀地呈現它。

        參數:
            data: 要打印的巢狀字典。
            level: 初始的層級（通常從0開始）。
            indent: 要用於縮進的字符串（例如，'\t'或'--'）。

        範例:
            YourClass.print_beautiful_dictionary({'a': {'b': 1, 'c': 2}, 'd': 3}, 0, '--')

        返回:
            無（只進行打印操作）。
        """
        for key, value in data.items():
            prefix = indent * level
            if isinstance(value, dict):
                print(f"{prefix}{key}")
                cls.print_beautiful_dictionary(value, level + 1, indent)
            else:
                print(f"{prefix}{key}: {value}")

    @classmethod
    def print_ocms_datasheet_dictionary(
        cls,
        ocms_datasheet,
        count=None,
        beauty=False,
        indent="    ",
    ):
        """
        專門用於打印OCMS數據表的字典。

        參數:
            ocms_datasheet: OCMS數據表的字典。
            count: 指定要打印的條目數量。
            beauty: 是否以美觀的方式打印巢狀字典。
            indent: 美觀打印時使用的縮進字符。

        範例:
            YourClass.print_ocms_datasheet_dictionary({'UUID1': {'a': 1}, 'UUID2': {'b': 2}}, count=1, beauty=True)

        返回:
            無（只進行打印操作）。
        """
        if not count:
            count = len(ocms_datasheet)
        for uuid, data in ocms_datasheet.items():
            if count == 0:
                break
            if not beauty:
                print(f"{uuid} {data}")
            else:
                print(f"{uuid}")
                cls.print_beautiful_dictionary(data, 1, indent)
            count -= 1
