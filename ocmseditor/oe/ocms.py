from collections import OrderedDict

import ocmseditor.tool as tool
import ocmseditor.oe.data.const as const


class OCMSStore:
    """
    Singleton (單例)
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OCMSStore, cls).__new__(cls)
            cls._instance.ui = UIStore()
            cls._instance.xml = XMLStore()
            cls._instance.res = ResourceStore()
            cls._instance.maya = MayaContextStore()
            cls._instance.met = MayaElementTree()
        return cls._instance

    @classmethod
    def write_datasheet(cls, filepath, datasheet, *args):
        sliced_datasheet = tool.Dictionary.slice(datasheet, *args)
        if filepath:
            tool.Dictionary.write_to_json_style(sliced_datasheet, filepath, indent=4)


class XMLStore:
    __done = False

    path = None
    doc = None
    root = None
    product_type = None
    config = None
    parse_data = None
    collect_data = None

    @classmethod
    def purse(cls):
        cls.path = None
        cls.doc = None
        cls.root = None
        cls.product_type = None
        cls.config = None
        cls.parse_data = None
        cls.collect_data = None

    @classmethod
    def load(cls, path):
        cls.path = path
        cls.doc = cls.get_doc()
        cls.root = cls.get_root()
        cls.product_type = cls.get_product_type()
        cls.config = cls.get_config()
        cls.parse_data = cls.get_parsed_data()
        cls.collect_data = cls.get_collect_data()

    @classmethod
    def get_doc(cls) -> str:
        if not cls.path:
            raise ValueError("XMLData path is not set.")
        return tool.File.read_utf16(cls.path)

    @classmethod
    def get_root(cls) -> tool.xml.Et.Element:
        return tool.XML.root(cls.doc)

    @classmethod
    def get_product_type(cls):
        """Get product type from DataSource from tag"""
        elem = cls.root.find("DataSource")
        if elem is not None:
            return elem.get("ProductType")
        raise ValueError("UnknownProductType")

    @classmethod
    def get_config(cls):
        """
        Get variations mapping of OCMS based on the product type.

        Returns:
            config: A dictionary containing the mapping information.
                - "Model": Corresponding model type.
                - "Component": Corresponding component type.
                - "non_device_type": A list of non-device types.
                - "preset_okay": A dictionary containing the parser configuration for valid elements.
                - "preset_none": A dictionary containing the parser configuration for invalid elements.
                - "preset_temp": A dictionary containing the parser configuration for temporary elements.
                - "preset_dupe": A list of parser configurations for duplicate elements.
        """
        if cls.product_type == "OCMS":
            config = {
                "model": "bundle",
                "component": "ComponentV2",
                "non_device_type": ["Floor", "Facility"],
                "preset_okay": {
                    "include_attrs": ["model", "bundle"],
                    "include_logic": "and",
                },
                "preset_none": {
                    "exclude_attrs": ["model", "bundle"],
                    "exclude_logic": "or",
                },
                "preset_temp": {
                    "include_attrs": ["model"],
                    "exclude_attrs": ["bundle"],
                },
                "preset_dupe": ["okay", "temp"],
            }
        elif cls.product_type == "OCMS2_0":
            config = {
                "model": "model",
                "component": "Component",
                "non_device_type": ["Floor", "Room", "Unknown"],
                "preset_okay": {
                    "include_attrs": ["model"],
                    "include_logic": "and",
                },
                "preset_none": {
                    "exclude_attrs": ["model", "bundle"],
                    "exclude_logic": "or",
                },
                "preset_temp": {
                    "include_attrs": ["model"],
                    "exclude_attrs": None,
                },
                "preset_dupe": ["okay"],
            }
        else:
            raise ValueError(f"Unsupported product type: {cls.product_type}")

        return config

    @classmethod
    def get_parsed_data(cls):
        # ---------------------------------------------------------------------
        # (Pre)Parse duplicate data -------------------------------------------
        # ---------------------------------------------------------------------
        unique_set = set()
        dupe_set = set()
        for element in cls.root.iter("Object"):
            name = element.attrib.get("name", "")
            if name == "":
                continue

            if name in unique_set:
                dupe_set.add(name)
                continue

            unique_set.add(name)

        patch_data = {
            "duplicates": {
                "unique": list(unique_set),
                "dupe": list(dupe_set),
            }
        }
        # ---------------------------------------------------------------------
        # Parse data ----------------------------------------------------------
        # ---------------------------------------------------------------------
        parsed_data = {}
        process_index = 1
        for element, object_path in tool.XML.iter_elems_paths(cls.root, tag="Object"):
            # Corresponding variations ----------------------------------------
            conf_model = cls.config["model"]
            conf_component = cls.config["component"]
            conf_non_device_type = cls.config["non_device_type"]

            # UUID ------------------------------------------------------------
            typ = element.get("type", "")
            if typ == "":
                raise ValueError("UnknownType, OCMS Element Type is not found.")

            corresponding_model = element.get(conf_model, "")

            uuid = tool.UUID.generate_ocms_uuid(
                type_str=typ,
                model=corresponding_model,
                number=process_index,
            )

            # Parent ----------------------------------------------------------
            parent = tool.XML.parent_path(object_path, separator="|")

            parent_uuid = parsed_data.get(parent, {}).get("maya", {}).get("uuid", "")

            # Transform -------------------------------------------------------
            transform = element.find("Transform")
            transform_attrs = tool.XML.extract_xform_attrs(transform)

            # Components ------------------------------------------------------
            components_attrs = []
            for component in element.findall(conf_component):
                component_attrs = tool.XML.extract_comp_attrs(component)
                components_attrs.append(component_attrs)

            # Master ----------------------------------------------------------

            conf_preset_okay = cls.config["preset_okay"]
            conf_preset_none = cls.config["preset_none"]
            conf_preset_temp = cls.config["preset_temp"]
            parsed_data[object_path] = {
                "global": {
                    "index": process_index,
                    "product_type": cls.product_type,
                    "is_dirty": const.INFO__NOT_YET_RESOLVED,
                },
                "maya": {
                    "uuid": uuid,
                    "parent": parent_uuid,
                    "is_synced_attribute": const.INFO__NOT_YET_RESOLVED,
                    "is_synced_resource": const.INFO__NOT_YET_RESOLVED,
                    "is_dirty": const.INFO__NOT_YET_RESOLVED,
                },
                "element_tree": {
                    "path": object_path,
                    "parent": parent,
                    "element": element,
                    "deep": object_path.count("|"),
                    "is_dirty": const.INFO__NOT_YET_RESOLVED,
                },
                "object": {
                    "type": element.get("type", ""),
                    "category": element.get("category", ""),
                    "name": element.get("name", ""),
                    "alias": element.get("alias", ""),
                    "model": element.get("model", ""),
                    "bundle": element.get("bundle", ""),
                    "time": element.get("time", ""),
                    "noted": element.get("noted", ""),
                    "remark": element.get("remark", ""),
                    "id": element.get("id", ""),
                    "is_dirty": const.INFO__NOT_YET_RESOLVED,
                },
                "transform": {
                    "position": {
                        "x": transform_attrs.get("position", {}).get("x", ""),
                        "y": transform_attrs.get("position", {}).get("y", ""),
                        "z": transform_attrs.get("position", {}).get("z", ""),
                    },
                    "rotation": {
                        "x": transform_attrs.get("rotation", {}).get("x", ""),
                        "y": transform_attrs.get("rotation", {}).get("y", ""),
                        "z": transform_attrs.get("rotation", {}).get("z", ""),
                    },
                    "scale": {
                        "x": transform_attrs.get("scale", {}).get("x", ""),
                        "y": transform_attrs.get("scale", {}).get("y", ""),
                        "z": transform_attrs.get("scale", {}).get("z", ""),
                    },
                    "is_dirty": const.INFO__NOT_YET_RESOLVED,
                },
                "component": {
                    f"{conf_component}": components_attrs,
                    "is_dirty": const.INFO__NOT_YET_RESOLVED,
                },
                "parser": {
                    "is_okay": bool(
                        tool.XML.filter_elem(
                            element,
                            include_attrs=conf_preset_okay["include_attrs"],
                            include_logic=conf_preset_okay["include_logic"],
                        )
                    ),
                    "is_none": bool(
                        tool.XML.filter_elem(
                            element,
                            exclude_attrs=conf_preset_none["exclude_attrs"],
                            exclude_logic=conf_preset_none["exclude_logic"],
                        )
                    ),
                    "is_temp": bool(
                        tool.XML.filter_elem(
                            element,
                            include_attrs=conf_preset_temp["include_attrs"],
                            exclude_attrs=conf_preset_temp["exclude_attrs"],
                        )
                    ),
                    "is_dupe": bool(
                        element.get("name", "") in patch_data["duplicates"]["dupe"]
                    ),
                    "is_non_device": typ in conf_non_device_type,
                    "is_dirty": const.INFO__NOT_YET_RESOLVED,
                },
                "file": {
                    "path": const.INFO__NOT_YET_RESOLVED,
                    "size": const.INFO__NOT_YET_RESOLVED,
                    "copy_to_path": const.INFO__NOT_YET_RESOLVED,
                    "is_dirty": const.INFO__NOT_YET_RESOLVED,
                },
                "resource": {
                    "model": corresponding_model,
                },
            }
            process_index += 1
        return parsed_data

    @classmethod
    def get_collect_data(cls):
        collect_data = {
            "object": {
                "tags": tool.XML.enum_tags(cls.root),
                "attributes": tool.XML.enum_attrs(cls.root),
                "types": tool.Collect.collect_attr_values(cls.parse_data, "type"),
                "category": tool.Collect.collect_attr_values(
                    cls.parse_data, "category"
                ),
                "remarks": tool.Collect.collect_attr_values(cls.parse_data, "remark"),
                "noted": tool.Collect.collect_attr_values(cls.parse_data, "noted"),
                "non_devices": [
                    data.get("ElementTree").get("element")
                    for _, data in cls.parse_data.items()
                    if data.get("Parser", {}).get("is_non_device", False)
                ],
            },
            "type_of": {
                "element": {},
                "name": {},
                "bundle": {},
                "model": {},
                "okay": {},
                "none": {},
                "temp": {},
                "dupe": {},
            },
        }
        bundle_set = set()
        model_set = set()
        for uuid, data in cls.parse_data.items():
            typ = data.get("object", {}).get("type", None)
            element = data.get("element_tree", {}).get("element", "")
            name = data.get("object", {}).get("name", "")
            bundle = data.get("object", {}).get("bundle", "")
            model = data.get("object", {}).get("model", "")
            okay = data.get("parser", {}).get("is_okay", const.INFO__RESOLVED_FAILED)
            none = data.get("parser", {}).get("is_none", const.INFO__RESOLVED_FAILED)
            temp = data.get("parser", {}).get("is_temp", const.INFO__RESOLVED_FAILED)
            dupe = data.get("parser", {}).get("is_dupe", const.INFO__RESOLVED_FAILED)
            if not typ:
                continue

            for category in collect_data.get("type_of").keys():
                collect_data["type_of"].setdefault(category, {})[typ] = (
                    collect_data["type_of"].get(category, {}).get(typ, [])
                )

            is_bundle_in_set = bundle in bundle_set
            is_model_in_set = model in model_set

            bundle_set.add(bundle)
            model_set.add(model)

            attributes_to_check = {
                "element": (element != "", element),
                "name": (name != "", name),
                "bundle": (not is_bundle_in_set, bundle),
                "model": (not is_model_in_set, model),
                "okay": (isinstance(okay, bool) and okay, element),
                "none": (isinstance(none, bool) and none, element),
                "temp": (isinstance(temp, bool) and temp, element),
                "dupe": (isinstance(dupe, bool) and dupe, element),
            }

            for category, (condition, value) in attributes_to_check.items():
                if condition:
                    collect_data["type_of"][category][typ].append(value)

        return collect_data

    @classmethod
    def done(cls):
        cls.__done = True

    @classmethod
    def valid(cls):
        return cls.__done


class ResourceStore:
    __done = False

    path = None

    scan_files = None
    parse_data = None
    collect_data = None

    maya_nodes = None

    @classmethod
    def purse(cls):
        cls.path = None

        cls.scan_files = None
        cls.parse_data = None
        cls.collect_dats = None

        cls.maya_nodes = None

    @classmethod
    def load(cls, path):
        cls.path = path

        cls.scan_files = cls.get_scan_files()
        cls.parse_data = cls.get_parsed_data()
        cls.collect_data = cls.get_collect_data()

    @classmethod
    def get_scan_files(cls):
        return tool.File.glob(cls.path, pattern="fbx", recursive=True)

    @classmethod
    def get_parsed_data(cls):
        # ---------------------------------------------------------------------
        # Pre-parse from xml parsed data --------------------------------------
        # ---------------------------------------------------------------------
        xml = XMLStore
        ocms_model = xml.config["model"]
        filtered_model_mapping = {}
        for _, data in xml.parse_data.items():
            if not data.get("parser", {}).get("is_okay", False):
                continue
            corresponding_model = data.get("object").get(ocms_model, "")
            if corresponding_model:
                model_name = (
                    corresponding_model.split("/")[-1]
                    if "/" in corresponding_model
                    else corresponding_model
                )
                filtered_model_mapping[model_name] = {
                    "object": {
                        "model": corresponding_model,
                    },
                }
        # ---------------------------------------------------------------------
        # Parse resources -----------------------------------------------------
        # ---------------------------------------------------------------------
        parsed_data = {}
        process_index = 1
        for path in cls.scan_files:
            model_element = filtered_model_mapping.get(
                tool.File.split_basename_without_ext(path).lower(), ""
            )
            if model_element == "":
                continue
            model = model_element.get("object", {}).get("model", "")
            if model in parsed_data.keys():
                continue
            parsed_data[model] = {
                "global": {
                    "index": process_index,
                    "project_path": tool.File.get_project_path(),
                    "is_dirty": const.INFO__NOT_YET_RESOLVED,
                },
                "file": {
                    "path": path,
                    "size": tool.File.get_size(path),
                    "copy_to_path": tool.File.get_copy_to_path(path),
                    "is_dirty": const.INFO__NOT_YET_RESOLVED,
                },
                "object": {
                    "model": model,
                    "is_dirty": const.INFO__NOT_YET_RESOLVED,
                },
            }
            process_index += 1

        # ---------------------------------------------------------------------
        # Check model's path if not exist but exist in ocms----------------
        # ---------------------------------------------------------------------
        process_index = len(parsed_data) + 1
        for uuid, data in XMLStore.parse_data.items():
            corresponding_model = data.get("object").get(ocms_model)
            if corresponding_model in parsed_data.keys():
                continue
            if corresponding_model == "":
                continue
            parsed_data[corresponding_model] = {
                "global": {
                    "index": process_index,
                    "project_path": tool.File.get_project_path(),
                    "is_dirty": const.INFO__NOT_YET_RESOLVED,
                },
                "file": {
                    "path": "",
                    "size": 0,
                    "copy_to_path": "",
                    "is_dirty": const.INFO__NOT_YET_RESOLVED,
                },
                "object": {
                    "model": corresponding_model,
                    "is_dirty": const.INFO__NOT_YET_RESOLVED,
                },
            }
            process_index += 1

        return parsed_data

    @classmethod
    def get_collect_data(cls):
        collect_data = {
            "sort": {
                "size": tool.Collect.collect_sorted_files_by_size(
                    cls.parse_data, reverse=True, readable=True
                ),
            },
            "stats": {
                "total_scan_files": len(cls.scan_files),
                "total_models": len(cls.parse_data),
                "total_valid_models": len(
                    [
                        data
                        for _, data in cls.parse_data.items()
                        if data.get("file", {}).get("size", 0) != 0
                    ]
                ),
            },
        }
        return collect_data

    @classmethod
    def done(cls):
        cls.__done = True
        cls.__is_updatable = False

    @classmethod
    def valid(cls):
        return cls.__done


class UIStore:
    context = {}


class MayaContextStore:
    active_object = None


class MayaElementTree:
    __product_type = None
    __config = {}
    __data = {}

    @classmethod
    def purse(cls):
        cls.__product_type = None
        cls.__config = {}
        cls.__data = {}

    @classmethod
    def update_data(cls):
        cls.purse()
        ocms = tool.OCMS.get_ocms()

        cls.__product_type = ocms.xml.product_type
        cls.__config = ocms.xml.config

        if not ocms.xml.parse_data:
            return
        for xpath, data in ocms.xml.parse_data.items():
            uuid = data["maya"]["uuid"]
            cls.__data.update({uuid: data})

    @classmethod
    def get_product_type(cls):
        return cls.__product_type

    @classmethod
    def get_config(cls):
        return cls.__config

    @classmethod
    def get_data(cls):
        return cls.__data

    @classmethod
    def get_uuid(cls):
        _available_index = 1
        for uuid, data in cls.__data.items():
            if data["global"]["index"] == _available_index:
                _available_index += 1
                continue
            else:
                break
        process_index = tool.UUID.format_number_with_digits(_available_index, 4)
        return tool.UUID.generate_ocms_uuid(
            type_str="Device",
            model="",
            number=process_index,
        )

    @classmethod
    def add_element(cls, uuid, parent_uuid=None):
        if cls.__data.get(uuid, None):
            return False
        if not tool.Maya.obj_exists(tool.Name.to_underscore(parent_uuid)):
            return False
        index = int(uuid.split("-")[-1])
        data = {
            "global": {
                "index": index,
                "product_type": cls.__product_type,
            },
            "maya": {
                "uuid": uuid,
                "parent": parent_uuid,
            },
        }

        cls.__data.update({uuid: data})
        cls.__data = OrderedDict(
            sorted(cls.__data.items(), key=lambda x: x[1]["global"]["index"])
        )
        return True

    @classmethod
    def del_element(cls, uuid, parent_uuid):
        if not cls.__data.get(uuid, None):
            return False
        if not tool.Maya.obj_exists(tool.Name.to_underscore(uuid)):
            return False
        if parent_uuid == "":
            return False
        del cls.__data[uuid]
        return True
