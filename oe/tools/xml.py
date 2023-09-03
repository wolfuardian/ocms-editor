import io
import warnings
import xml.etree.ElementTree as Et

import oe.tools as tools
import oe.core.tools as core


class XML(core.XML):
    @classmethod
    def root(cls, xmlstring):
        return Et.fromstring(xmlstring)

    @classmethod
    def iterator(cls, root, tag=None, attr=None, kwd=None):
        if attr or kwd is not None:
            if attr is None:
                tools.Logging.parse_xml_logger().warning(
                    "attr should not be empty when kwd used."
                )

            if kwd is None:
                tools.Logging.parse_xml_logger().warning(
                    "kwd should not be empty when attr used."
                )

        return [elem for elem in root.iter(tag) if elem.get(attr) == kwd]

    @classmethod
    def enumerator(cls, elems, attr, mode=0, out_attr=None, test_print=False):
        lst = []
        if out_attr is None:
            out_attr = attr

        # Default: Do not iter.
        if mode == 0:
            for elem in elems:
                if elem.get(attr) is not None and elem.get(attr) not in lst:
                    lst.append(elem.get(out_attr))

        # Exist mode: Iter matched items.
        if mode == 1:
            for elem in elems:
                if elem.get(attr) is None:
                    continue
                lst.append(elem.get(out_attr))

        # None mode: Iter not matched items.
        if mode == 2:
            for elem in elems:
                if elem.get(attr) is not None:
                    continue
                lst.append(elem.get(out_attr))

        # When enabled, the log will print more information and the unicode will be converted to str.
        if test_print:
            return tools.String.list_to_string(lst)

        return lst

    @classmethod
    def extractor(
        cls, elems, pos_attrs=None, neg_attrs=None, pos_op="or", neg_op="and"
    ):
        """
        原名 filter
        positive, negative -> Use list[str] or str to match.
        positive_option, negative_option -> Use '|', '&', 'and', 'or' to compare.
        """

        lst = []

        # None = '*'.
        pos_attrs = "*" if pos_attrs is None else pos_attrs
        neg_attrs = "*" if neg_attrs is None else neg_attrs

        # '*' = Skip filtering.
        filter_pos = False if pos_attrs == "*" else True
        filter_neg = False if neg_attrs == "*" else True

        # Convert str to lst
        pos_attrs = [pos_attrs] if type(pos_attrs) == str else pos_attrs
        neg_attrs = [neg_attrs] if type(neg_attrs) == str else neg_attrs

        if pos_op != "|":
            if pos_op != "&":
                if pos_op != "and":
                    if pos_op != "or":
                        warnings.simplefilter("error", UserWarning)
                        warnings.warn(
                            "option_pos should only be like '|', '&', 'and', 'or'."
                        )

        if neg_op != "|":
            if neg_op != "&":
                if neg_op != "and":
                    if neg_op != "or":
                        warnings.simplefilter("error", UserWarning)
                        warnings.warn(
                            "option_neg should only be like '|', '&', 'and', 'or'."
                        )

        valid = None

        for elem in elems:

            if filter_pos:
                # Condition Positive OR
                def _validate_positive_or():
                    __valid = False
                    for __attr in pos_attrs:
                        if elem.get(__attr) is not None:
                            __valid = True
                    return __valid

                if pos_op == "|":
                    valid = _validate_positive_or()
                if pos_op == "or":
                    valid = _validate_positive_or()

                # Condition Positive AND
                def _validate_positive_and():
                    __valid = True
                    for __attr in pos_attrs:
                        if elem.get(__attr) is None:
                            __valid = False
                    return __valid

                if pos_op == "&":
                    valid = _validate_positive_and()
                if pos_op == "and":
                    valid = _validate_positive_and()

            if filter_neg:
                valid = valid if filter_pos else True
                _valid = None

                # Condition Negative OR
                def _validate_negative_or():
                    __valid = True
                    for __attr in neg_attrs:
                        if elem.get(__attr) is not None:
                            __valid = False
                    return __valid

                if neg_op == "|":
                    _valid = _validate_negative_or()
                if neg_op == "or":
                    _valid = _validate_negative_or()

                # Condition Negative AND

                def _validate_negative_and():
                    __valid = False
                    for __attr in neg_attrs:
                        if elem.get(__attr) is None:
                            __valid = True
                    return __valid

                if neg_op == "&":
                    _valid = _validate_negative_and()
                if neg_op == "and":
                    _valid = _validate_negative_and()

                valid = _valid if valid else valid

            if valid:
                lst.append(elem)

        return lst

    @classmethod
    def collect_attrs(cls, root, kwd):
        collection = []

        def _enumerate(element):
            if getattr(element, kwd) not in collection:
                collection.append(getattr(element, kwd))
            for child in element:
                _enumerate(child)

        _enumerate(root)
        return collection

    @classmethod
    def collect_unique_attrs(cls, root):
        collection = []
        for obj in cls.iterator(root, tag="Object"):
            for key in obj.attrib.keys():
                if key not in collection:
                    collection.append(key)
        return collection
