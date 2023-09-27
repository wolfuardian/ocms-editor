import sys
import logging
import importlib
import maya.cmds as cmds

import ocmseditor.tool as tool
import ocmseditor.oe.data.const as const

DEFAULT_RELOAD_PACKAGES = []


class Logger:
    @classmethod
    def log(cls, level, name, message=None):
        actual_name = const.NAME_MAPPING.get(name, name)
        message = message or f"<{name}>"
        logger = logging.getLogger(actual_name)
        if level == "debug":
            logger.debug(message)
        elif level == "info":
            logger.info(message)
        elif level == "warning":
            logger.warning(message)
        elif level == "error":
            logger.error(message)
        else:
            pass

    @classmethod
    def debug(cls, name, message=None):
        cls.log("debug", name, message)

    @classmethod
    def info(cls, name, message=None):
        cls.log("info", name, message)

    @classmethod
    def warning(cls, name, message=None):
        cls.log("warning", name, message)

    @classmethod
    def error(cls, name, message=None):
        cls.log("error", name, message)


class PackageReloader:
    @classmethod
    def reload(cls, packages=None):
        if packages is None:
            Logger.info(__name__, f"No packages specified, using default packages")
            packages = DEFAULT_RELOAD_PACKAGES

        for mod in cls.upload(packages=packages):
            Logger.info(__name__, f"Reloading module: {mod}")
            importlib.reload(mod)
        Logger.info(__name__, f"Completed reloading modules")

    @classmethod
    def upload(cls, packages=None):
        Logger.info(__name__, "Constructing unload list")
        reload_list = []
        for mod in sys.modules.keys():
            for package in packages:
                if mod.startswith(package):
                    reload_list.append(mod)

        Logger.info(__name__, "Unloading modules")
        unloaded_modules = []
        for mod in reload_list:
            try:
                if sys.modules[mod] is not None:
                    unloaded_modules.append(sys.modules[mod])
            except KeyError:
                Logger.warning(__name__, f"Module {mod} not found in sys.modules")
            except TypeError:
                Logger.warning(__name__, f"Invalid type for module key: {mod}")
        Logger.info(__name__, "Completed unloading modules")
        return unloaded_modules


class ModelImporter:
    def execute(self):
        self.add_groups()
        self.add_model_to_scene()
        self.hide_group()

    @staticmethod
    def add_groups():
        ocms = tool.OCMS.get_ocms()
        res_pdata = ocms.res.parse_data
        for model, data in res_pdata.items():
            filepath = data["file"]["path"]
            group_name = tool.Name.to_underscore(
                tool.File.split_basename_without_ext(filepath)
            ).lower()
            new_group = tool.Maya.add_group(f"r_{group_name}")
            res_pdata[model].setdefault("maya", {})
            res_pdata[model]["maya"]["raw_model"] = new_group

    @staticmethod
    def add_model_to_scene():
        ocms = tool.OCMS.get_ocms()
        res_pdata = ocms.res.parse_data
        for model, data in res_pdata.items():
            group_name = res_pdata[model]["maya"]["raw_model"]
            new_objects = tool.Maya.import_file(data["file"]["path"])
            children = cmds.parent(new_objects, group_name)
            res_pdata[model].setdefault("maya", {})
            res_pdata[model]["maya"]["children"] = children

    @staticmethod
    def hide_group():
        ocms = tool.OCMS.get_ocms()
        res_pdata = ocms.res.parse_data
        for model, data in res_pdata.items():
            group_name = res_pdata[model]["maya"]["raw_model"]
            cmds.hide(group_name)


class OCMSDataSyncHandler:
    def execute(self):
        self.add_groups()
        self.set_parent()
        self.copy_model_to_node()
        self.apply_transform()
        self.add_system_attributes()

    @staticmethod
    def add_groups():
        ocms = tool.OCMS.get_ocms()
        xml_pdata = ocms.xml.parse_data
        for _, data in xml_pdata.items():
            object_name = data["maya"]["uuid"]
            group_name = tool.Name.to_underscore(object_name)
            new_group = tool.Maya.add_group(group_name)

    @staticmethod
    def set_parent():
        ocms = tool.OCMS.get_ocms()
        xml_pdata = ocms.xml.parse_data
        for _, data in xml_pdata.items():
            object_unique_name = data["maya"]["uuid"]
            object_parent_name = data["maya"]["parent"]
            group_name = tool.Name.to_underscore(object_unique_name)
            parent_group_name = tool.Name.to_underscore(object_parent_name)
            if parent_group_name == "":
                continue
            children = cmds.parent(group_name, parent_group_name)

    @staticmethod
    def copy_model_to_node():
        ocms = tool.OCMS.get_ocms()
        xml_pdata = ocms.xml.parse_data
        res_pdata = ocms.res.parse_data
        for _, data in xml_pdata.items():
            model_name = data["resource"]["model"]
            if model_name in res_pdata.keys():
                node_name = tool.Name.to_underscore(data["maya"]["uuid"])
                raw_model_group = res_pdata[model_name]["maya"]["raw_model"]
                # duplicate_group = cmds.duplicate(raw_model_group, rr=True)[0]
                duplicate_group = cmds.spaceLocator()
                # cmds.scaleConstraint(raw_model_group, duplicate_group, offset=[1, 1, 1])
                # cmds.setAttr(f"{duplicate_group}.scaleX", 1)
                # cmds.setAttr(f"{duplicate_group}.scaleY", 1)
                # cmds.setAttr(f"{duplicate_group}.scaleZ", 1)

                # duplicate_group = cmds.spaceLocator()
                cmds.showHidden(duplicate_group)
                target_group = node_name
                cmds.parent(duplicate_group, target_group)
                cmds.rename(duplicate_group, f"inst_{node_name}")

    @staticmethod
    def add_system_attributes():
        ocms = tool.OCMS.get_ocms()

        config = ocms.xml.config
        conf_component = config["component"]

        xml_pdata = ocms.xml.parse_data
        _system_attributes = []
        for _, data in xml_pdata.items():
            node_name = tool.Name.to_underscore(data["maya"]["uuid"])

            # Object
            typ = data["object"]["type"]
            category = data["object"]["category"]
            name = data["object"]["name"]
            alias = data["object"]["alias"]
            model = data["object"]["model"]
            bundle = data["object"]["bundle"]
            time = data["object"]["time"]
            noted = data["object"]["noted"]
            remark = data["object"]["remark"]
            id = data["object"]["id"]

            compound_name = "Object"
            attrs = {
                "type": typ,
                "category": category,
                "name": name,
                "alias": alias,
                "model": model,
                "bundle": bundle,
                "time": time,
                "noted": noted,
                "remark": remark,
                "id": id,
            }

            tool.Maya.setup_string_attr_to_obj(compound_name, attrs, node_name)

            # Component
            components = data["component"][conf_component]

            for __component in components:
                compound_name = tool.Name.to_underscore(__component["name"])
                properties = __component["property"]
                attrs = {}
                for __property in properties:
                    attrs.update(
                        {
                            compound_name
                            + tool.Name.to_underscore(__property["name"]): __property[
                                "text"
                            ]
                        }
                    )

                tool.Maya.setup_string_attr_to_obj(compound_name, attrs, node_name)

    @staticmethod
    def apply_transform():
        ocms = tool.OCMS.get_ocms()
        xml_pdata = ocms.xml.parse_data
        for _, data in xml_pdata.items():
            object_name = tool.Name.to_underscore(data["maya"]["uuid"])
            transform = data["transform"]
            position = transform["position"]
            rotation = transform["rotation"]
            scale = transform["scale"]
            for xyz in position:
                number = float(position[xyz]) if position[xyz] != "" else 0.0
                cmds.setAttr(f"{object_name}.translate{xyz.upper()}", number)
            for xyz in rotation:
                number = float(rotation[xyz]) if rotation[xyz] != "" else 0.0
                cmds.setAttr(f"{object_name}.rotate{xyz.upper()}", number)
            for xyz in scale:
                number = float(scale[xyz]) if scale[xyz] != "" else 1.0
                cmds.setAttr(f"{object_name}.scale{xyz.upper()}", number)
