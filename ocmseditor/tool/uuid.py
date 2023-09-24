import ocmseditor.core.tool as core


class UUID(core.UUID):
    @classmethod
    def format_number_with_digits(cls, number, num_digits):
        """
        將給定的數字格式化為指定位數的字符串。

        範例:
            number = 23
            num_digits = 4
            formatted_number = YourClass.format_number_with_digits(number, num_digits)
            print(formatted_number)  # 輸出會是 "0023"

        參數:
            number: 需要格式化的數字。
            num_digits: 需要的位數。

        返回:
            一個符合指定位數的格式化數字字符串。
        """
        digit_format = f"{{:0{num_digits}d}}"
        return digit_format.format(number)

    @classmethod
    def generate_ocms_uuid(cls, type_str, model, number):
        """
        根據給定的型別、模型和編號生成一個特定格式的 UUID。

        範例:
            type_str = "Device"
            model = "XR/11"
            number = 123
            uuid = YourClass.generate_ocms_uuid(type_str, model, number)
            print(uuid)  # 輸出會是 "OCMS-Device-XR-11-0123"

        參數:
            type_str: UUID 的型別描述字符串。
            model: UUID 的模型描述，斜線將會被轉換為短橫線。
            number: UUID 的編號部分。

        返回:
            一個符合特定格式的 UUID 字符串。
        """
        format_type = type_str.capitalize()
        format_model = model.replace("/", "-")
        format_digit = cls.format_number_with_digits(number, 4)

        return f"OCMS-{format_type}-{format_model}-{format_digit}"
