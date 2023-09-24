import re


import ocmseditor.core.tool as core


class String(core.String):
    @classmethod
    def list_to_string(cls, lst):
        """
        將一個 list 轉換為由逗號和空格分隔的字符串。

        範例:
            lst = [1, 2, 3]
            result = YourClass.list_to_string(lst)
            print(result)  # 輸出會是 "1, 2, 3"

        參數:
            lst: 需要轉換的 list。

        返回:
            一個由 list 元素組成的、由逗號和空格分隔的字符串。
        """
        return ", ".join(map(str, lst)) if lst else ""

    @classmethod
    def dict_to_string(cls, dictionary):
        """
        將一個 dictionary 轉換為由逗號和空格分隔的 "key: value" 格式的字符串。

        範例:
            dictionary = {'a': 1, 'b': 2}
            result = YourClass.dict_to_string(dictionary)
            print(result)  # 輸出會是 "a: 1, b: 2"

        參數:
            dictionary: 需要轉換的 dictionary。

        返回:
            一個由 dictionary 的 key-value 對組成的、由逗號和空格分隔的字符串。
        """
        return (
            ", ".join(f"{key}: {value}" for key, value in dictionary.items())
            if dictionary
            else ""
        )

    @classmethod
    def decode_utf8_string(cls, byte_string):
        """
        將字節字符串解碼為 UTF-8 格式的字符串。如果解碼失敗，將剪切最後一個字節並重新嘗試。

        範例:
            byte_str = b'This is UTF-8 encoded.'
            decoded_str = YourClass.decode_utf8_string(byte_str)
            print(decoded_str)  # 輸出會是 'This is UTF-8 encoded.'

        參數:
            byte_string: 要解碼的字節字符串。

        返回:
            解碼後的 UTF-8 字符串。
        """
        try:
            decoded_string = byte_string.decode("utf-8")
            return decoded_string
        except UnicodeDecodeError:
            # print(f"Decode error: {byte_string}, clip last byte and try again.")
            new_byte_string = byte_string[:-1]
            return cls.decode_utf8_string(new_byte_string)

    @classmethod
    def decode_fbxasc_string(cls, fbxasc_string):
        """
        解碼具有特殊 FBXASC 編碼的字符串。

        範例:
            fbxasc_str = 'FBXASC065FBXASC097FBXASC115'
            decoded_str = YourClass.decode_fbxasc_string(fbxasc_str)
            print(decoded_str)  # 輸出會是 'Bas'

        參數:
            fbxasc_string: 要解碼的 FBXASC 字符串。

        返回:
            解碼後的 UTF-8 字符串。
        """
        if "FBXASC" not in fbxasc_string:
            return fbxasc_string
        prefix = "FBXASC"
        decoded_string = fbxasc_string
        matches = re.findall(f"{prefix}\d{{3}}", fbxasc_string)

        for match in matches:
            decoded_char = chr(int(match[len(prefix) :]))
            decoded_string = decoded_string.replace(match, decoded_char)

        byte_string = decoded_string.encode("iso-8859-1")
        return cls.decode_utf8_string(byte_string)
