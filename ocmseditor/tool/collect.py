import ocmseditor.core.tool as core
import ocmseditor.tool as tool


class Collect(core.Collect):
    @classmethod
    def collect_attr_values(cls, datasheet, attr):
        """
        收集特定屬性下所有唯一值。

        範例:
            datasheet = {
                "uuid_1": {"main_attr_1": {"target_attr": 1, "another_attr": "a"}},
                "uuid_2": {"main_attr_2": {"target_attr": 2, "another_attr": "b"}},
                ...
            }
            attr = "target_attr"
            YourClass.collect_attr_values(datasheet, attr)
            # 返回值將會是：[1, 2]

        參數:
            cls: 這個方法所屬的類別。
            datasheet: 包含數據項目和其主屬性以及內部屬性的字典。
            attr: 需要收集其值的特定屬性名稱。

        返回:
            一個已排序且去重的特定屬性值列表。
        """
        values_set = set()
        for uuid, data in datasheet.items():
            for main_attribute, attribute_data in data.items():
                value = attribute_data.get(attr, None)
                if value:
                    values_set.add(value)
        return sorted(list(values_set))

    @classmethod
    def collect_sorted_files_by_size(cls, datasheet, reverse, readable=True):
        """
        根據檔案大小對數據進行排序。

        範例:
            datasheet = {
                "uuid_1": {"file": {"size": 1024}},
                "uuid_2": {"file": {"size": 2048}},
                ...
            }
            YourClass.collect_sorted_files_by_size(datasheet, reverse=True, readable=True)
            # 返回值將會是：{'uuid_2': '2 KB', 'uuid_1': '1 KB'}

        參數:
            cls: 這個方法所屬的類別。
            datasheet: 包含數據項目和其主屬性的字典。
            reverse: 一個布爾值，決定排序是否需要反轉。
            readable: 一個布爾值，決定是否將檔案大小轉換為易讀格式。

        返回:
            一個根據檔案大小排序的字典。
        """
        filesizes = {}
        for uuid, data in datasheet.items():
            filesize = data.get("file", {}).get("size", None)
            if filesize != 0:
                filesizes[uuid] = filesize
        sorted_pairs = sorted(
            filesizes.items(), key=lambda item: item[1], reverse=reverse
        )
        sorted_filesizes = dict(sorted_pairs)
        for uuid, filesize in sorted_filesizes.items():
            if readable:
                sorted_filesizes[uuid] = tool.File.bytes_to_readable_size(filesize)
        return sorted_filesizes
