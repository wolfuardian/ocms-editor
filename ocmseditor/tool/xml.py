import xml.etree.ElementTree as Et

import ocmseditor.core.tool as core


class XML(core.XML):
    @classmethod
    def all_attrs(cls, elem, attrs):
        """
        判斷 'elem' 是否具有 'attrs' 中指定的所有屬性。

        範例:
            elem = {'name': 'John', 'age': 30}
            attrs = ['name', 'age']
            result = YourClass.all_attrs(elem, attrs)  # 返回 True

            elem = {'name': 'John'}
            attrs = ['name', 'age']
            result = YourClass.all_attrs(elem, attrs)  # 返回 False

        參數:
            cls: 這個方法所屬的類別。
            elem: 要檢查屬性的元素，假設它實現了 `.get()` 方法。
            attrs: 要檢查的屬性名稱列表。

        返回:
            如果 elem 中存在所有屬性，則返回 True，否則返回 False。
        """
        return all(elem.get(a) is not None for a in attrs)

    @classmethod
    def any_attrs(cls, elem, attrs):
        """
        判斷 'elem' 是否具有 'attrs' 中指定的任何屬性。

        範例:
            elem = {'name': 'John', 'age': 30}
            attrs = ['name', 'salary']
            result = YourClass.any_attrs(elem, attrs)  # 返回 True

            elem = {'hobby': 'Reading'}
            attrs = ['name', 'salary']
            result = YourClass.any_attrs(elem, attrs)  # 返回 False

        參數:
            cls: 這個方法所屬的類別。
            elem: 要檢查屬性的元素，假設它實現了 `.get()` 方法。
            attrs: 要檢查的屬性名稱列表。

        返回:
            如果 elem 中存在任何屬性，則返回 True，否則返回 False。
        """
        return any(elem.get(a) is not None for a in attrs)

    @classmethod
    def enum_attrs(cls, elem):
        """
        列舉 'elem' 中所有唯一的屬性。

        範例:
            假設 elem 是一個 ElementTree 的根元素，包含多個子元素，每個子元素都有 'id' 和 'class' 屬性。
            result = YourClass.enum_attrs(elem)
            # 返回 ['id', 'class'] 或其他在 elem 中唯一存在的屬性名稱。

        參數:
            cls: 這個方法所屬的類別。
            elem: 要列舉屬性的元素，假設它具有 `.iter()` 方法。

        返回:
            返回一個列表，包含 'elem' 及其所有子元素中所有唯一的屬性名稱。
        """
        unique_attrs = set()
        for elem in elem.iter():
            for attr in elem.keys():
                unique_attrs.add(attr)
        return list(unique_attrs)

    @classmethod
    def enum_tags(cls, elem):
        """
        列舉 'elem' 中所有唯一的標籤。

        範例:
            假設 elem 是一個 ElementTree 的根元素，包含多個 'div' 和 'span' 子元素。
            result = YourClass.enum_tags(elem)
            # 返回 ['div', 'span'] 或其他在 elem 中唯一存在的標籤名稱。

        參數:
            cls: 這個方法所屬的類別。
            elem: 要列舉標籤的元素，假設它具有 `.iter()` 方法。

        返回:
            返回一個列表，包含 'elem' 及其所有子元素中所有唯一的標籤名稱。
        """
        unique_tags = set()
        for elem in elem.iter():
            unique_tags.add(elem.tag)
        return list(unique_tags)

    @classmethod
    def exclude_attrs(cls, elem, exclude_attrs, exclude_logic):
        """
        根據指定的屬性和邏輯運算符，判斷是否應排除 'elem'。

        範例:
            elem = {'name': 'John', 'age': 30}
            exclude_attrs = ['name']
            exclude_logic = '|'
            result = YourClass.exclude_attrs(elem, exclude_attrs, exclude_logic)  # 返回 False

        參數:
            cls: 這個方法所屬的類別。
            elem: 要過濾的元素。
            exclude_attrs: 應排除的屬性名稱或列表。
            exclude_logic: 使用的邏輯運算符 ("|" 或 "&")。

        返回:
            如果應排除元素，則返回 False，否則返回 True。
        """
        if exclude_attrs is None:
            exclude_attrs = "*"

        if exclude_attrs == "*":
            return True

        exclude_attrs = (
            [exclude_attrs] if isinstance(exclude_attrs, str) else exclude_attrs
        )

        if exclude_logic in ("|", "or"):
            return not cls.any_attrs(elem, exclude_attrs)
        elif exclude_logic in ("&", "and"):
            return not cls.all_attrs(elem, exclude_attrs)
        else:
            raise ValueError(f"Invalid exclude logic: {exclude_logic}")

    @classmethod
    def include_attrs(cls, elem, include_attrs, include_logic):
        """
        根據指定的屬性和邏輯運算符，判斷是否應包括 'elem'。

        範例:
            elem = {'name': 'John', 'age': 30}
            include_attrs = ['name']
            include_logic = '|'
            result = YourClass.include_attrs(elem, include_attrs, include_logic)  # 返回 True

        參數:
            cls: 這個方法所屬的類別。
            elem: 要過濾的元素。
            include_attrs: 應包括的屬性名稱或列表。
            include_logic: 使用的邏輯運算符 ("|" 或 "&")。

        返回:
            如果應包括元素，則返回 True，否則返回 False。
        """
        if include_attrs is None:
            include_attrs = "*"

        if include_attrs == "*":
            return True

        include_attrs = (
            [include_attrs] if isinstance(include_attrs, str) else include_attrs
        )

        if include_logic in ("|", "or"):
            return cls.any_attrs(elem, include_attrs)
        elif include_logic in ("&", "and"):
            return cls.all_attrs(elem, include_attrs)
        else:
            raise ValueError(f"Invalid include logic: {include_logic}")

    @classmethod
    def filter_elem(
        cls,
        elem,
        include_attrs=None,
        exclude_attrs=None,
        include_logic="or",
        exclude_logic="and",
    ):
        """
        進行綜合過濾，根據 include 和 exclude 的邏輯決定是否保留 'elem'。

        範例1:
            elem = {'name': 'John', 'age': 30}
            include_attrs = ['name']
            exclude_attrs = ['age']
            include_logic = 'or'
            exclude_logic = 'and'
            result = YourClass.filter_elem(elem, include_attrs, exclude_attrs, include_logic, exclude_logic)
            # 返回 None

        範例2:
            elem = {'name': 'John', 'age': 30}
            include_attrs = ['name']
            exclude_attrs = ['age', 'job']
            include_logic = 'or'
            exclude_logic = 'and'
            result = YourClass.filter_elem(elem, include_attrs, exclude_attrs, include_logic, exclude_logic)
            # 返回 elem

        參數:
            cls: 這個方法所屬的類別。
            elem: 要過濾的元素。
            include_attrs: 應包括的屬性名稱或列表。
            exclude_attrs: 應排除的屬性名稱或列表。
            include_logic: 使用的邏輯運算符 ("|" 或 "&") 用於包括屬性。
            exclude_logic: 使用的邏輯運算符 ("|" 或 "&") 用於排除屬性。

        返回:
            如果元素滿足 include 和 exclude 的條件，則返回元素本身，否則返回 None。
        """
        if not cls.include_attrs(elem, include_attrs, include_logic):
            return None
        if not cls.exclude_attrs(elem, exclude_attrs, exclude_logic):
            return None
        else:
            return elem

    @classmethod
    def extract_comp_attrs(cls, elem):
        """
        從給定的元素中提取 '組件' 相關的屬性和子元素 'property'。

        範例:
            elem = Element('component', {'name': 'Motor', 'assembly': 'Engine'})
            prop1 = SubElement(elem, 'property', {'name': 'Power'})
            prop1.text = '100HP'
            comp_dict = YourClass.extract_comp_attrs(elem)
            # 返回 {'name': 'Motor', 'assembly': 'Engine', 'property': [{'name': 'Power', 'text': '100HP'}]}

        參數:
            elem: 包含 '組件' 資訊的 XML 元素。

        返回:
            包含 '組件' 屬性和 'property' 子元素的字典。
        """
        comp_name = elem.get("name", "")
        comp_dict = {
            "name": comp_name,
            "assembly": elem.get("assembly", ""),
            "property": [],
        }

        for prop in elem.findall("property"):
            name = prop.get("name", "")
            value = prop.text

            prop_dict = {"name": name, "text": str(value)}
            comp_dict["property"].append(prop_dict)

        return comp_dict

    @classmethod
    def extract_xform_attrs(cls, elem):
        """
        從給定的元素中提取 '變換' 相關的屬性。

        範例:
            elem = Element('transform')
            pos = SubElement(elem, 'position', {'x': '1', 'y': '2', 'z': '3'})
            attributes = YourClass.extract_xform_attrs(elem)
            # 返回 {'position': {'x': '1', 'y': '2', 'z': '3'}}

        參數:
            elem: 包含 '變換' 資訊的 XML 元素。

        返回:
            包含 '變換' 屬性的字典。
        """
        if not elem:
            ident_transform = {
                "position": {"x": "0", "y": "0", "z": "0"},
                "rotation": {"x": "0", "y": "0", "z": "0"},
                "scale": {"x": "1", "y": "1", "z": "1"},
            }
            return ident_transform
        attributes = {}
        for elem in elem:
            attributes.update({elem.tag: {k: v for k, v in elem.attrib.items()}})
        return attributes

    @classmethod
    def get_attr(cls, elem, attr, out_attr=None):
        """
        從單一元素中提取指定的屬性。

        範例:
            elem = Element('person', {'name': 'John', 'age': '30'})
            name = YourClass.get_attr(elem, 'name')
            # 返回 'John'

        參數:
            elem: 要查詢的 XML 元素。
            attr: 要查詢的屬性名。
            out_attr: 如果指定，將返回此屬性的值而非 'attr' 的值。

        返回:
            查詢到的屬性值，如果未找到則拋出 ValueError。
        """
        if elem.get(attr) is None:
            raise ValueError("Attribute not found")
        output = attr if out_attr is None else out_attr
        return elem.get(output, "Attribute not found")

    @classmethod
    def query_elems_attrs(cls, elems, attr, out_attr=None):
        """
        從元素集合中提取指定的屬性。

        範例:
            elems = [Element('person', {'name': 'John', 'age': '30'}), Element('person', {'name': 'Jane'})]
            names = YourClass.query_elems_attrs(elems, 'name')
            # 返回 ['John', 'Jane']

        參數:
            elems: 要查詢的 XML 元素集合。
            attr: 要查詢的屬性名。
            out_attr: 如果指定，將返回此屬性的值而非 'attr' 的值。

        返回:
            包含查詢結果的列表。
        """
        query_results = []
        for element in elems:
            try:
                result = cls.get_attr(element, attr, out_attr)
                query_results.append(result)
            except ValueError as e:
                query_results.append(str(e))
        return query_results

    @classmethod
    def iter_elems_paths(
        cls,
        elem: Et.Element,
        tag: str = None,
        root_path: str = "root",
        separator: str = "|",
    ):
        """
        遞迴地遍歷 XML 元素樹，並為每個元素生成其在樹中的路徑。

        範例:
            root = Element('root', {'name': 'Root'})
            child1 = Element('child', {'name': 'Child1'})
            child2 = Element('child', {'name': 'Child2'})
            root.append(child1)
            root.append(child2)

            for elem, path in YourClass.iter_elems_paths(root):
                print(elem.tag, path)
            # 輸出會是：
            # (root, root)
            # (child, root|Child1)
            # (child, root|Child2)

        參數:
            elem: 要遍歷的起始元素。
            tag: 如果指定，只生成與該標籤匹配的元素。
            root_path: 起始元素的路徑（默認為 "root"）。
            separator: 用於分隔路徑組件的字符（默認為 "|"）。

        返回:
            一個生成器，每次迭代都會返回一個元素和其在樹中的路徑。
        """
        if tag is None or elem.tag == tag:
            yield elem, root_path

        for child in elem:
            child_name = child.get("name")
            new_path = f"{root_path}{separator}{child_name}"

            yield from cls.iter_elems_paths(child, tag, new_path)

    @classmethod
    def parent_path(cls, path, separator="|", remove_num=1):
        """
        獲取給定路徑的父路徑。

        範例:
            path = "root|folder1|folder2|item"
            parent_path = YourClass.parent_path(path)
            print(parent_path)  # 輸出會是 "root|folder1|folder2"

        參數:
            path: 給定的完整路徑字符串。
            separator: 用於分隔路徑組件的字符（默認為 "|"）。
            remove_num: 從末尾移除的路徑組件數量（默認為 1）。

        返回:
            一個字符串，表示給定路徑的父路徑。
        """
        if not path or not isinstance(path, str) or path == "root":
            return ""
        path_components = path.split(separator)
        parent_path = separator.join(path_components[:-remove_num])
        return parent_path

    @classmethod
    def root(cls, doc):
        """
        將給定的 XML 文檔字符串解析成一個 ElementTree 的根元素對象。

        範例:
            xml_str = '<root><child name="A"/><child name="B"/></root>'
            root_elem = YourClass.root(xml_str)
            print(root_elem.tag)  # 輸出會是 "root"

        參數:
            doc: XML 文檔的字符串形式。

        返回:
            一個 ElementTree 的根元素對象。
        """
        return Et.fromstring(doc)
