import json
from itertools import islice

import ocmseditor.core.tool as core


class Dictionary(core.Dictionary):
    @classmethod
    def assemble(cls, keys, values):
        """
        接受兩個列表（鍵和值）並返回一個由這些鍵和值組成的字典。

        範例:
            YourClass.assemble(['a', 'b'], [1, 2])  # 返回 {'a': 1, 'b': 2}

        參數:
            keys: 包含字典鍵的列表。
            values: 包含字典值的列表。

        返回:
            由鍵和值組成的字典。
        """
        return dict(zip(keys, values))

    @classmethod
    def slice(cls, dictionary, count=-1):
        """
        返回字典的前 N 個鍵值對。如果 count 為 -1，則返回整個字典。

        範例:
            dictionary = {'a': 1, 'b': 2, 'c': 3}
            count = 2
            result = YourClass.slice(dictionary, count)  # 返回 {'a': 1, 'b': 2}

        參數:
            cls: 這個方法所屬的類別。
            dictionary: 要切片的字典。
            count: 要返回的鍵值對數量。

        返回:
            返回一個包含前 N 個鍵值對的新字典。
        """
        if count == -1:
            return dictionary
        return {k: dictionary[k] for k in islice(dictionary.keys(), count)}

    @classmethod
    def flatten(cls, dictionary, level=0, indent="    "):
        """
        展平嵌套字典並返回一個包含展平結果的字符串列表。

        範例:
            dictionary = {'a': 1, 'b': {'c': 2, 'd': 3}}
            result = YourClass.flatten(dictionary)
            # 返回 ['a: 1', 'b:', '    c: 2', '    d: 3']

        參數:
            cls: 這個方法所屬的類別。
            dictionary: 要展平的嵌套字典。
            level: 字典的嵌套層級，用於控制縮進。
            indent: 每一層縮進所用的字符。

        返回:
            返回一個包含展平結果的字符串列表。
        """
        result = []
        for key, value in dictionary.items():
            line_indent = indent * level
            if isinstance(value, dict):
                result.append(f"{line_indent}{key}:")
                result += cls.flatten(value, level + 1, indent)
            else:
                result.append(f"{line_indent}{key}: {value}")
        return result

    @classmethod
    def convert_all_to_string(cls, dictionary):
        """
        遍歷嵌套字典，將所有非字符串的值轉換為其對應的字符串表示。

        範例:
            dictionary = {'a': 1, 'b': {'c': 2, 'd': True}}
            YourClass.convert_all_to_string(dictionary)
            # dictionary 變為 {'a': '1', 'b': {'c': '2', 'd': 'True'}}

        參數:
            cls: 這個方法所屬的類別。
            dictionary: 要轉換的嵌套字典。

        返回:
            無返回值，字典將會就地(in-place)更新。
        """
        for key, value in dictionary.items():
            if isinstance(value, dict):
                cls.convert_all_to_string(value)
            elif not isinstance(value, str):
                dictionary[key] = str(value)

    @classmethod
    def write_to_json_style(cls, dictionary, path, indent=4):
        """
        將字典以 JSON 風格寫入文件。

        範例:
            dictionary = {'a': 1, 'b': {'c': 2, 'd': True}}
            path = "output.json"
            YourClass.write_to_json_style(dictionary, path)

            # output.json 文件中的內容將會是：
            # {
            #     "a": "1",
            #     "b": {
            #         "c": "2",
            #         "d": "True"
            #     }
            # }

        參數:
            cls: 這個方法所屬的類別。
            dictionary: 要寫入文件的字典。
            path: 要寫入的文件的路徑。
            indent: JSON 文件的縮進字符數。

        返回:
            無返回值，會在指定的路徑下生成 JSON 文件。
        """
        cls.convert_all_to_string(dictionary)
        with open(path, "w") as f:
            json.dump(dictionary, f, indent=indent)
