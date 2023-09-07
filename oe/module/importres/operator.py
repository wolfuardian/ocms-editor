import os
import re
import json
import math
import time
import shutil

import xml.etree.ElementTree as Et
import maya.cmds as cmds

import oe.tools as tools
import oe.storage as storage

from oe.utils import qt
from oe.refer import Registry as reg_

from . import store, prop


# Common functions.
def uuid(node: str) -> str:
    """
    Get the UUID of a node in Maya.
    :param node: The node to get the UUID of.
    :return: The UUID of the node.
    """
    return cmds.ls(node, uuid=True)[0]


def create_folder(folder_dir: str) -> int:
    """
    Create a folder.
    :param folder_dir: The folder directory.
    :return: 0 if the folder exists, 1 if the folder is created.
    """
    if os.path.exists(folder_dir):
        print(f"{folder_dir} folder exists.")
        return 0
    else:
        os.makedirs(folder_dir)
        print(f"Created {folder_dir} folder.")
        return 1


def copy_file_to_destination(source_file: str, destination_file: str) -> int:
    """
    Copy a file to a destination.
    :param source_file: The source file.
    :param destination_file: The destination file.
    :return: 0 if the source file does not exist,
    1 if the file is renamed, 2 if the file name case is changed, 3 if no change.
    """
    if not os.path.exists(source_file):
        raise ValueError(f"The source file {source_file} does not exist.")

    source_basename = os.path.basename(source_file)
    destination_basename = os.path.basename(destination_file)

    if os.path.isfile(destination_file):
        print(f"{destination_file} already exists.")
        return 0
    else:
        shutil.copy(source_file, destination_file)
        if source_basename.lower() != destination_basename.lower():
            print(
                f"Copied {source_basename} -> {destination_basename} to the destination folder. (Renamed)"
            )
            return 1
        elif source_basename != destination_basename:
            print(
                f"Copied {source_basename} -> {destination_basename} to the destination folder. (Name case changed)"
            )
            return 2
        else:
            print(f"Copied {source_basename} to the destination folder. (No change)")
            return 3


def fix_invalid_json_string(json_string: str) -> str:
    """
    Fix invalid JSON string.
    :param json_string: The JSON string to fix.
    :return: The fixed JSON string.
    """
    json_string = json_string.replace("'", '"')
    return json_string


def string_difference(long_string: str, short_string: str) -> str:
    """
    Get the difference between two strings.
    :param long_string: The long string.
    :param short_string: The short string.
    :return: The difference between the two strings.
    """
    return long_string.replace(short_string, "")


def convert_to_unicode_name(invalid_name: str) -> str:
    """
    Convert a string to a unicode name.
    :param invalid_name: The invalid name to convert.
    :return: The unicode name.
    """
    unicode_name = ""
    for char in invalid_name:
        if ord(char) > 127:
            unicode_name += "U{:04X}".format(ord(char))
        else:
            unicode_name += char
    return unicode_name


def truncate_path(path: str, num_components_to_remove: int) -> str:
    """
    Truncate a path.
    :param path: The path to truncate.
    :param num_components_to_remove: The number of components to remove.
    :return: The truncated path.
    """
    path_components = path.split("/")
    selected_components = path_components[:-num_components_to_remove]
    new_path = "/".join(selected_components)
    return new_path


def iter_etree_with_path(
    node: Et.Element, tag: str = None, root_path: str = "root"
) -> any:
    """
    Iterate over a node and its children.
    :param node: The node to iterate over.
    :param tag: The tag to iterate over.
    :param root_path: The root path.
    """
    if tag == "*":
        tag = None
    if tag is None or node.tag == tag:
        yield node, root_path
    for child in node:
        current = child.get("name")
        child_path = f"{root_path}/{current}"
        for _child, _child_path in iter_etree_with_path(
            child, tag, root_path=child_path
        ):
            yield _child, _child_path


def create_group_and_assign_selected_obj(group_name: str, obj_name: str) -> str:
    """
    Create a group and assign the selected object to the group.
    :param group_name: This is the name of the group.
    :param obj_name: This is the name of the object.
    :return: The name of the group.
    """
    group_name = cmds.group(empty=True, name=group_name)
    cmds.parent(obj_name, group_name)
    return group_name


# Attribute functions.
def add_string_attr_to_object(
    attr_compound_name: str, attr_dict: dict, object_name: str
) -> None:
    """
    Add a string attribute to an object.
    :param attr_compound_name: The compound attribute name.
    :param attr_dict: The attribute dictionary.
    :param object_name: The object name.
    :return: None
    """
    if not cmds.objExists(object_name):
        cmds.warning(object_name + " Object does not exist.")
        return

    if not cmds.attributeQuery(attr_compound_name, node=object_name, exists=True):
        cmds.addAttr(
            object_name,
            longName=attr_compound_name,
            numberOfChildren=len(attr_dict.keys()),
            attributeType="compound",
        )
    else:
        # cmds.warning(f'{attr_compound_name} attribute exists')
        pass

    for add_attr, add_value in attr_dict.items():
        nice_name = add_attr
        if attr_compound_name in add_attr:
            nice_name = string_difference(add_attr, attr_compound_name)
        if not cmds.attributeQuery(add_attr, node=object_name, exists=True):
            cmds.addAttr(
                object_name,
                longName=add_attr,
                niceName=nice_name,
                dataType="string",
                parent=attr_compound_name,
            )
        else:
            # cmds.warning(f'{add_attr} exists')
            pass


def set_string_attr_to_object(
    attr_compound_name: str, attr_dict: dict, object_name: str
) -> None:
    """
    Set a string attribute to an object.
    :param attr_compound_name: The compound attribute name.
    :param attr_dict: The attribute dictionary.
    :param object_name: The object name.
    :return:
    """
    if not cmds.objExists(object_name):
        cmds.warning(object_name + " Object does not exist.")
        return

    if not cmds.attributeQuery(attr_compound_name, node=object_name, exists=True):
        cmds.addAttr(
            object_name,
            longName=attr_compound_name,
            numberOfChildren=len(attr_dict.keys()),
            attributeType="compound",
        )
    else:
        # cmds.warning(f'{attr_compound_name} set_attr exists')
        pass

    for set_attr, set_value in attr_dict.items():
        if cmds.attributeQuery(set_attr, node=object_name, exists=True) is True:
            if set_value is None:
                set_value = ""
            cmds.setAttr((object_name + "." + set_attr), set_value, type="string")
        else:
            # cmds.warning(set_attr + ' not exists')
            pass


def has_custom_attrs(node: str, custom_comp_attr: str = None) -> bool:
    """
    Check if a node has custom attributes.
    :param node: The node to check.
    :param custom_comp_attr: The compound attribute to check.
    :return: True if the node has custom attributes.
    """
    custom_attrs = cmds.listAttr(node, userDefined=True)
    if not custom_comp_attr:
        return custom_attrs is not None and len(custom_attrs) > 0
    return cmds.attributeQuery(custom_comp_attr, node=node, exists=True)


def list_compound_attrs(node: str) -> list:
    """
    List compound attributes.
    :param node: The node to list attributes from.
    :return: The list of compound attributes.
    """
    all_attrs = cmds.listAttr(node, multi=True, userDefined=True)
    attributes = []
    for attrib in all_attrs:
        attr_type = cmds.getAttr(node + "." + attrib, type=True)
        if attr_type not in ["compound", "TdataCompound"]:
            attributes.append(attrib)
    return attributes


def get_compound_attr_values(node: str, compound_attr: str) -> dict:
    """
    Get compound attribute values.
    :param node: The node to get attributes from.
    :param compound_attr: The compound attribute to get values from.
    :return: The dictionary of compound attribute values.
    """
    children_attrs = None
    if not cmds.objExists(node):
        print(f"Node {node} does not exist.")
    if cmds.attributeQuery(compound_attr, node=node, exists=True):
        children_attrs = cmds.attributeQuery(
            compound_attr, node=node, listChildren=True
        )
    else:
        print(f"Attribute {compound_attr} does not exist in node {node}.")
    if not children_attrs:
        return {}
    return {
        child_attr: cmds.getAttr(f"{node}.{child_attr}")
        for child_attr in children_attrs
    }


# Object functions.
def is_transform(node: str) -> bool:
    """
    Check if the object is a transform node.
    :param node: The object name.
    :return: True if the object is a transform node.
    """
    node_type = cmds.nodeType(node)
    return node_type == "transform"


def is_group(node: str) -> bool:
    """
    Check if the object is a group.
    :param node: The object name.
    :return: True if the object is a group.
    """
    if not is_transform(node):
        return False

    children = cmds.listRelatives(node, children=True) or []
    if not children:
        return False

    for child in children:
        if cmds.nodeType(child) in ("mesh", "nurbsCurve", "nurbsSurface"):
            return False
    return True


# File functions.
def import_fbx(path: str) -> list:
    """
    Import an FBX file.
    :param path: The path to the FBX file.
    :return: The root nodes.
    """
    if not os.path.exists(path):
        return cmds.warning(
            f"The path {path} does not exist and the action cannot be completed."
        )
    all_new_nodes = cmds.file(
        path,
        i=True,
        force=True,
        type="FBX",
        ignoreVersion=True,
        mergeNamespacesOnClash=True,
        returnNewNodes=True,
    )
    all_new_nodes = cmds.ls(all_new_nodes, dagObjects=True, exactType="transform")
    root_nodes = [
        node for node in all_new_nodes if not cmds.listRelatives(node, parent=True)
    ]
    return root_nodes


def import_model(file: str) -> str:
    """
    Import a model.
    :param file: The path to the model.
    :return: The root node of the model.
    """
    _split_path, _extension = os.path.splitext(file)
    _filedir, _filename = os.path.split(_split_path)

    root_nodes = import_fbx(file)

    root_node = root_nodes[0]

    if len(root_nodes) != 1:
        group_name = cmds.group(empty=True, name=f"_{_filename}_gp")
        for root_node in root_nodes:
            cmds.parent(root_node, group_name)
        root_node = group_name
        cmds.warning(f"The node {root_node} has too many root nodes.")
        return root_node

    if is_group(root_node):
        root_node = cmds.rename(root_node, f"_{_filename}_gp")
    else:
        root_node = create_group_and_assign_selected_obj(
            group_name=f"_{_filename}_gp", obj_name=root_nodes[0]
        )

    print(f"{_split_path} has been imported.")
    return root_node


# This class is used to store the information of the OCMS.
class OCMSInformationNode:
    """
    This class is used to store the information of the OCMS.
    """

    def __init__(self):
        self.ocms_inf_nodes = None

    def create_node(self):
        """
        This method is used to create a node to store the information of the OCMS.
        """
        self.ocms_inf_nodes = cmds.createNode("message", name="OCMSInformationNode")

    def add_nodes_attr(self, attr_name: str):
        """
        This method is used to add the nodes attribute to the OCMS information node.
        """
        if cmds.attributeQuery(attr_name, node=self.ocms_inf_nodes, exists=True):
            cmds.warning("The attribute " + attr_name + " already exists.")
            return
        cmds.addAttr(self.ocms_inf_nodes, longName=attr_name, dataType="string")

    def set_nodes_attr(self, attr_name: str, value: str):
        """
        This method is used to set the value of the nodes attribute.
        """
        value = fix_invalid_json_string(value)
        if not cmds.attributeQuery(attr_name, node=self.ocms_inf_nodes, exists=True):
            cmds.warning("The attribute " + attr_name + " does not exist.")
            return
        cmds.setAttr(self.ocms_inf_nodes + "." + attr_name, value, type="string")

    def get_nodes_attr(self, attr_name: str) -> dict:
        """
        This method is used to get the value of the nodes attribute.
        """
        if not cmds.attributeQuery(attr_name, node=self.ocms_inf_nodes, exists=True):
            cmds.warning("The attribute " + attr_name + " does not exist.")
            return {}
        nodes_string = cmds.getAttr(self.ocms_inf_nodes + "." + attr_name)
        nodes = json.loads(nodes_string)
        return nodes


# This class is used to record the elapsed time.
class TimeRecorder:
    """
    This class is used to record the elapsed time.
    """

    def __init__(self, start_time: float = -1, end_time: float = -1):
        self._start_time = -1
        self._end_time = -1
        self._current_percent = -1
        if start_time != -1:
            self._start_time = start_time
        if end_time != -1:
            self._end_time = end_time

    def __call__(self, percent):
        if self._current_percent == percent:
            return
        self._current_percent = percent
        if percent < 100 and self._start_time == -1:
            self._start_time = time.perf_counter()
        if percent == 100:
            self._end_time = time.perf_counter()
            print(
                f"Elapsed time: {round(self._end_time - self._start_time, 4)} seconds"
            )


# This class is used to display a progress bar in the Maya script editor.
class ProgressBar:
    """
    This class is used to display a progress bar in the Maya script editor.
    """

    def __init__(self, bar_length=40, pattern="#", interval=50):
        self.bar_length = bar_length
        self.pattern = pattern
        self.interval = interval
        self._value = 0
        self._max_value = 0
        self._percent = 0

    def __call__(self, current_value, max_value):
        self._value = current_value
        self._max_value = max_value
        current_percent = self._calculate_percent()
        if self._percent == current_percent:
            return
        self._percent = current_percent
        self._progressbar = self._get_progressbar()
        if self._percent % self.interval == 0:
            self._print_progressbar(self._progressbar)

    def _calculate_percent(self):
        self._progress_percentage = float(self._value) / self._max_value
        return math.floor(float(self._value) / self._max_value * 100)

    def _get_progressbar(self):
        self._filled_length = int(round(self.bar_length * self._progress_percentage))
        return self.pattern * self._filled_length + "-" * (
            self.bar_length - self._filled_length
        )

    def _print_progressbar(self, current_progressbar):
        _result = f"[{current_progressbar}] {self._percent}% ({self._value}/{self._max_value})"
        print(_result)


# This class is used to synchronize the XML nodes to the Maya scene.
class TaskSyncXMLNodes:
    """
    This class is used to synchronize the XML nodes to the Maya scene.
    """

    def __init__(self, xml_root: Et.Element):
        self._xml_root = xml_root
        self._xml_product = None
        self._xml_nodes_with_path = None
        self._ocms_inf_node = OCMSInformationNode()
        self._nodes = []
        self._nodes_map = {}
        self._parent_paths = []
        self._parent_objects = []
        self._system_attributes = []
        self._object_attributes = []
        self._transform_attributes = []
        self._component_attributes = []
        self._organized_nodes = []
        self._model_attr_map = {
            "OCMS": "bundle",
            "OCMS2_0": "model",
        }

        self._component_attr_map = {
            "OCMS": "ComponentV2",
            "OCMS2_0": "Component",
        }
        self._xml_product = self.func__get_product_type()
        self._xml_nodes_with_path = self.func__get_xml_nodes_with_path()

    # This function is used to show the progress information.
    @staticmethod
    def show_progress_info_with_message(timer, progressbar, current, total):
        """
        :param timer:
        :param progressbar:
        :param current:
        :param total:
        """
        progressbar(current, total)
        timer(math.floor(current / total * 100))

    # Inheritance functions.
    @staticmethod
    def func_find_matching_objects(
        compound_attr: str, path_attr: str, target_path: str
    ) -> list:
        """
        Find matching objects.
        :param compound_attr: The compound attribute to check.
        :param path_attr: The path attribute to check.
        :param target_path: The target path to check.
        :return: The list of matching objects.
        """
        matching_objects = []
        all_objects = cmds.ls()
        for node in all_objects:
            if cmds.attributeQuery(compound_attr, node=node, exists=True):
                attr_value = cmds.getAttr(node + "." + compound_attr + "." + path_attr)
                if attr_value == target_path:
                    matching_objects.append(node)
        return matching_objects

    @staticmethod
    def func_replace_invalid_characters(
        input_str: str, replacement_char: str = "_"
    ) -> str:
        """
        Replace invalid characters in a string.
        :param input_str: The input string.
        :param replacement_char: The replacement character.
        :return: The string with replaced characters.
        """
        invalid_chars_pattern = re.compile(r"[^a-zA-Z0-9_]")
        result = invalid_chars_pattern.sub(replacement_char, input_str)
        return result

    @staticmethod
    def func_create_group_from_element(element: Et.Element) -> str:
        """
        Create a group from an element.
        :param element: The element to create a group from.
        :return: The group name.
        """
        model_name = element.get("name").split("/")[-1]
        unicode_name = convert_to_unicode_name(model_name)
        maya_group = cmds.group(empty=True, name=unicode_name + "_gp")
        return maya_group

    @staticmethod
    def func_append_nodes_dict(
        nodes_dict: dict, maya_object: str, src_path: str
    ) -> dict:
        """
        Append nodes dictionary with maya object and source path.
        This is used to create a dictionary of maya objects and their source paths.
        :param nodes_dict: The nodes dictionary to append to.
        :param maya_object: The maya object to append to the dictionary as a key.
        :param src_path: The source path to append to the dictionary as a value.
        :return: The nodes dictionary with the new key and value.
        """
        nodes_dict[uuid(maya_object)] = src_path
        return nodes_dict

    @staticmethod
    def func_find_nodes_by_path(dictionary: dict, path: str) -> str:
        """
        Find nodes by path.
        :param dictionary: The dictionary to search.
        :param path: The path to search for.
        :return: The node name.
        """
        for key, value in dictionary.items():
            if value == path:
                return key
            if path == "root":
                return ""

    @staticmethod
    def func_build_system_attributes(path: str, parent: str) -> dict:
        """
        Build system attributes.
        :param path: The path to the object.
        :param parent: The parent of the object.
        :return: The dictionary of system attributes.
        """
        return {
            "System" + "path": path,
            "System" + "parent": parent,
            "System" + "type": "Node",
        }

    @staticmethod
    def func_handle_string_attr_to_object(prefix: str, attributes: dict, obj: str):
        """
        Handle string attribute to object.
        :param prefix: The prefix to add to the attribute.
        :param attributes: The attributes to add to the object.
        :param obj: The object to add the attributes to.
        """
        add_string_attr_to_object(prefix, attributes, obj)
        set_string_attr_to_object(prefix, attributes, obj)

    @staticmethod
    def func_extract_transform_properties(transform: Et.Element) -> dict:
        """
        Extract transform properties.
        :param transform: The transform element.
        :return: The dictionary of transform properties.
        """
        attributes = {}
        for transform_property in transform:
            property_attributes = transform_property.attrib
            for attr, value in property_attributes.items():
                attributes[(transform_property.tag + attr)] = value
        return attributes

    def func_extract_component_properties(self, comp: Et.Element) -> dict:
        """
        Extract component properties.
        :param comp: The component element.
        :return: The dictionary of component properties.
        """
        comp_name = comp.get("name")
        prop_attributes = {}
        component_attributes = comp.attrib
        for comp_attr, comp_value in component_attributes.items():
            prop_attributes[
                (self.func_replace_invalid_characters(comp_name) + comp_attr)
            ] = comp_value
        properties = comp.findall("property")
        for prop in properties:
            name = prop.get("name")
            comp_attr = f"property_{name}"
            prop_attributes[
                (self.func_replace_invalid_characters(comp_name) + comp_attr)
            ] = prop.text
        return prop_attributes

    def func__get_xml_nodes_with_path(self):
        """
        This function is used to get the XML nodes with path.
        """
        self._xml_nodes_with_path = [
            (elem, source_path)
            for elem, source_path in iter_etree_with_path(self._xml_root, "Object")
        ]
        return self._xml_nodes_with_path

    def func__get_product_type(self):
        """
        This function is used to get the product type.
        """
        self._xml_product = next(
            (
                elem.get("ProductType")
                for elem in self._xml_root.iter("DataSource")
                if elem.get("ProductType")
            ),
            None,
        )
        return self._xml_product

    def task__create_groups(self):
        """
        This function creates groups.
        """
        timer = TimeRecorder()
        progressbar = ProgressBar()

        _nodes = []
        for current, (elem, source_path) in enumerate(self._xml_nodes_with_path):
            _nodes.append(self.func_create_group_from_element(elem))
            self.show_progress_info_with_message(
                timer, progressbar, current + 1, len(self._xml_nodes_with_path)
            )
        self._nodes = _nodes

        self._ocms_inf_node.add_nodes_attr("nodes")
        self._ocms_inf_node.set_nodes_attr("nodes", self._nodes.__str__())

    def task__updating_nodes_dict(self):
        """
        This function updates the nodes dictionary.
        """
        timer = TimeRecorder()
        progressbar = ProgressBar()

        _nodes_map = {}
        for current, (elem, source_path) in enumerate(self._xml_nodes_with_path):
            _nodes_map = self.func_append_nodes_dict(
                _nodes_map, self._nodes[current], source_path
            )
            self.show_progress_info_with_message(
                timer, progressbar, current + 1, len(self._xml_nodes_with_path)
            )
        self._nodes_map = _nodes_map

        self._ocms_inf_node.add_nodes_attr("nodes_map")
        self._ocms_inf_node.set_nodes_attr("nodes_map", self._nodes_map.__str__())

    def task__creating_parent_paths(self):
        """
        This function creates parent paths.
        """
        timer = TimeRecorder()
        progressbar = ProgressBar()
        _parent_paths = []
        for current, (elem, source_path) in enumerate(self._xml_nodes_with_path):
            _parent_paths.append(truncate_path(source_path, 1))
            self.show_progress_info_with_message(
                timer, progressbar, current + 1, len(self._xml_nodes_with_path)
            )
        self._parent_paths = _parent_paths

        self._ocms_inf_node.add_nodes_attr("parent_paths")
        self._ocms_inf_node.set_nodes_attr("parent_paths", self._parent_paths.__str__())

    def task__finding_parents(self):
        """
        This function finds parents.
        """
        timer = TimeRecorder()
        progressbar = ProgressBar()
        _parent_objects = []
        for current, (_, source_path) in enumerate(self._xml_nodes_with_path):
            _parent_objects.append(
                self.func_find_nodes_by_path(
                    self._nodes_map, self._parent_paths[current]
                )
            )
            self.show_progress_info_with_message(
                timer, progressbar, current + 1, len(self._xml_nodes_with_path)
            )
        self._parent_objects = _parent_objects

        self._ocms_inf_node.add_nodes_attr("parent_objects")
        self._ocms_inf_node.set_nodes_attr(
            "parent_objects", self._parent_objects.__str__()
        )

    def task__create_system_attributes(self):
        """
        This function creates system attributes.
        """
        timer = TimeRecorder()
        progressbar = ProgressBar()
        _system_attributes = []
        for current, (elem, source_path) in enumerate(self._xml_nodes_with_path):
            _system_attributes.append(
                self.func_build_system_attributes(
                    source_path, self._parent_objects[current]
                )
            )
            self.func_handle_string_attr_to_object(
                "System", _system_attributes[-1], self._nodes[current]
            )
            self.show_progress_info_with_message(
                timer, progressbar, current + 1, len(self._xml_nodes_with_path)
            )
        self._system_attributes = _system_attributes

        self._ocms_inf_node.add_nodes_attr("system_attributes")
        self._ocms_inf_node.set_nodes_attr(
            "system_attributes", self._system_attributes.__str__()
        )

    def task__create_object_attributes(self):
        """
        This function creates object attributes.
        """
        timer = TimeRecorder()
        progressbar = ProgressBar()
        _object_attributes = []
        for current, (elem, source_path) in enumerate(self._xml_nodes_with_path):
            _object_attributes.append(elem.attrib)
            self.func_handle_string_attr_to_object(
                "Object", _object_attributes[-1], self._nodes[current]
            )
            self.show_progress_info_with_message(
                timer, progressbar, current + 1, len(self._xml_nodes_with_path)
            )
        self._object_attributes = _object_attributes

        self._ocms_inf_node.add_nodes_attr("object_attributes")
        self._ocms_inf_node.set_nodes_attr(
            "object_attributes", self._object_attributes.__str__()
        )

    def task__create_transform_attributes(self):
        """
        This function creates transform attributes.
        """
        timer = TimeRecorder()
        progressbar = ProgressBar()
        _transform_attributes = []
        for current, (elem, source_path) in enumerate(self._xml_nodes_with_path):
            transform = elem.find("Transform")
            if not transform:
                self.show_progress_info_with_message(
                    timer, progressbar, current + 1, len(self._xml_nodes_with_path)
                )
                continue
            _transform_attributes.append(
                self.func_extract_transform_properties(transform)
            )
            self.func_handle_string_attr_to_object(
                "Transform", _transform_attributes[-1], self._nodes[current]
            )
            self.show_progress_info_with_message(
                timer, progressbar, current + 1, len(self._xml_nodes_with_path)
            )
        self._transform_attributes = _transform_attributes

        self._ocms_inf_node.add_nodes_attr("transform_attributes")
        self._ocms_inf_node.set_nodes_attr(
            "transform_attributes", self._transform_attributes.__str__()
        )

    def task__create_component_attributes(self):
        """
        This function creates component attributes.
        """
        timer = TimeRecorder()
        progressbar = ProgressBar()
        _component_attributes = []
        for current, (elem, source_path) in enumerate(self._xml_nodes_with_path):
            component_attr = self._component_attr_map.get(self._xml_product, None)
            if not component_attr:
                self.show_progress_info_with_message(
                    timer, progressbar, current + 1, len(self._xml_nodes_with_path)
                )
                continue
            component = elem.find(component_attr)
            if not component:
                self.show_progress_info_with_message(
                    timer, progressbar, current + 1, len(self._xml_nodes_with_path)
                )
                continue
            components = elem.findall(component_attr)
            for component in components:
                component_name = component.get("name")
                _component_attributes.append(
                    self.func_extract_component_properties(component)
                )
                prefix = self.func_replace_invalid_characters(component_name)
                self.func_handle_string_attr_to_object(
                    prefix, _component_attributes[-1], self._nodes[current]
                )
            self.show_progress_info_with_message(
                timer, progressbar, current + 1, len(self._xml_nodes_with_path)
            )
        self._component_attributes = _component_attributes

        self._ocms_inf_node.add_nodes_attr("component_attributes")
        self._ocms_inf_node.set_nodes_attr(
            "component_attributes", self._component_attributes.__str__()
        )

    def task__organizing_the_group(self):
        """
        This function organizes the group.
        """
        timer = TimeRecorder()
        progressbar = ProgressBar()
        _organized_nodes = []
        ls_transform = cmds.ls(type="transform")
        for current, current_node in enumerate(ls_transform):
            if not has_custom_attrs(current_node, "System"):
                self.show_progress_info_with_message(
                    timer, progressbar, current + 1, len(ls_transform)
                )
                continue
            compound_attrs = get_compound_attr_values(current_node, "System")
            parent_node = compound_attrs.get("System" + "parent")
            if parent_node == "":
                self.show_progress_info_with_message(
                    timer, progressbar, current + 1, len(ls_transform)
                )
                continue
            parent_node = cmds.ls(parent_node, uuid=True)
            _organized_nodes.append({current_node: parent_node})
            cmds.parent(current_node, parent_node)
            self.show_progress_info_with_message(
                timer, progressbar, current + 1, len(ls_transform)
            )
        self._organized_nodes = _organized_nodes

        self._ocms_inf_node.add_nodes_attr("organized_nodes")
        self._ocms_inf_node.set_nodes_attr(
            "organized_nodes", self._organized_nodes.__str__()
        )

    def task__apply_transform(self):
        """
        This function applies the transform.
        """
        timer = TimeRecorder()
        progressbar = ProgressBar()
        ls_transform = cmds.ls(type="transform")
        for current, current_node in enumerate(ls_transform):
            if not has_custom_attrs(current_node, "System"):
                self.show_progress_info_with_message(
                    timer, progressbar, current + 1, len(ls_transform)
                )
                continue

            transform_attrs = get_compound_attr_values(current_node, "Transform")
            if len(transform_attrs) == 0:
                print(f"Node {current_node} has no transform attributes.")
                continue
            maya_object = cmds.ls(current_node)[0]

            print(f"Applying transform to {cmds.ls(current_node)}...")
            if transform_attrs.get("positionx"):
                cmds.setAttr(
                    maya_object + ".translateX", float(transform_attrs.get("positionx"))
                )
            if transform_attrs.get("positiony"):
                cmds.setAttr(
                    maya_object + ".translateY", float(transform_attrs.get("positiony"))
                )
            if transform_attrs.get("positionz"):
                cmds.setAttr(
                    maya_object + ".translateZ", float(transform_attrs.get("positionz"))
                )
            if transform_attrs.get("rotationx"):
                cmds.setAttr(
                    maya_object + ".rotateX", float(transform_attrs.get("rotationx"))
                )
            if transform_attrs.get("rotationy"):
                cmds.setAttr(
                    maya_object + ".rotateY", float(transform_attrs.get("rotationy"))
                )
            if transform_attrs.get("rotationz"):
                cmds.setAttr(
                    maya_object + ".rotateZ", float(transform_attrs.get("rotationz"))
                )
            if transform_attrs.get("scalex"):
                cmds.setAttr(
                    maya_object + ".scaleX", float(transform_attrs.get("scalex"))
                )
            if transform_attrs.get("scaley"):
                cmds.setAttr(
                    maya_object + ".scaleY", float(transform_attrs.get("scaley"))
                )
            if transform_attrs.get("scalez"):
                cmds.setAttr(
                    maya_object + ".scaleZ", float(transform_attrs.get("scalez"))
                )

    def execute_tasks(self):
        """
        This function executes the tasks.
        """
        print("Creating OCMS information node...")
        self._ocms_inf_node.create_node()

        print("\nCreating groups...")
        self.task__create_groups()

        print("\nUpdating nodes dictionary...")
        self.task__updating_nodes_dict()

        print("\nCreating parent paths...")
        self.task__creating_parent_paths()

        print("\nFinding parents...")
        self.task__finding_parents()

        print("\nCreating system attributes... This may take a while... Please wait...")
        self.task__create_system_attributes()

        print("\nCreating object attributes... This may take a while... Please wait...")
        self.task__create_object_attributes()

        print(
            "\nCreating transform attributes... This may take a while... Please wait..."
        )
        self.task__create_transform_attributes()

        print(
            "\nCreating component attributes... This may take a while... Please wait..."
        )
        self.task__create_component_attributes()

        print("\nMoving objects to their parents...")
        self.task__organizing_the_group()

        print("\nApplying transform...")
        self.task__apply_transform()

        print("All tasks completed successfully!")


# This class is used to collect the FBX files.
class TaskCollectFBXs:
    """
    Collect the FBX files.
    """

    def __init__(self, project_dir: str, mapped_path_dict: dict):
        self._project_dir = project_dir
        self._mapped_path_dict = mapped_path_dict
        self._mapped_path_completed_dict = {}
        self._folder_copied_count = 0
        self._file_copied_count = 0
        self._folder_skip_count = 0
        self._file_skip_count = 0

    # This function is used to show the progress information.
    @staticmethod
    def show_progress_info_with_message(timer, progressbar, current, total):
        """
        :param timer:
        :param progressbar:
        :param current:
        :param total:
        """
        progressbar(current, total)
        timer(math.floor(current / total * 100))

    def func__get_mapped_path_completed_dict(self):
        """
        Get the mapped path completed dictionary.
        :return: The mapped path completed dictionary.
        """
        return self._mapped_path_completed_dict

    def task__get_completed_path(self):
        """
        Get the completed path.
        :return:
        """
        timer = TimeRecorder()
        progressbar = ProgressBar()
        for current, (typ, objects) in enumerate(self._mapped_path_dict.items()):
            for _current, (filename, src_path) in enumerate(objects.items()):
                folder_dir = os.path.join(self._project_dir, typ, filename).replace(
                    "\\", "/"
                )
                dst_path = folder_dir + "/" + filename + os.path.splitext(src_path)[1]
                self._mapped_path_completed_dict[filename] = [
                    folder_dir,
                    src_path,
                    dst_path,
                ]
            self.show_progress_info_with_message(
                timer, progressbar, current + 1, len(self._mapped_path_dict)
            )

    def task__create_folder(self):
        """
        Create the folder.
        :return: None
        """
        timer = TimeRecorder()
        progressbar = ProgressBar()
        for current, (filename, split_path) in enumerate(
            self._mapped_path_completed_dict.items()
        ):
            folder_dir = split_path[0]
            if create_folder(folder_dir) == 0:
                self._folder_skip_count += 1
            else:
                self._folder_copied_count += 1
            self.show_progress_info_with_message(
                timer, progressbar, current + 1, len(self._mapped_path_completed_dict)
            )

    def task__copy_file(self):
        """
        Copy the file.
        :return: None
        """
        timer = TimeRecorder()
        progressbar = ProgressBar()
        for current, (filename, split_path) in enumerate(
            self._mapped_path_completed_dict.items()
        ):
            file_source = split_path[1]
            file_destination = split_path[2]
            if copy_file_to_destination(file_source, file_destination) == 0:
                self._file_skip_count += 1
            else:
                self._file_copied_count += 1
            self.show_progress_info_with_message(
                timer, progressbar, current + 1, len(self._mapped_path_completed_dict)
            )

    def execute_tasks(self):
        """
        This function executes the tasks.
        """
        print("Get the completed path...")
        self.task__get_completed_path()

        print("\nCreate the folder...")
        self.task__create_folder()
        print(
            f"\nA total of {self._folder_copied_count.__str__()} folders have been created "
            f"and {self._folder_skip_count.__str__()} folders have been skipped."
        )

        print("\nCopy the file...")
        self.task__copy_file()
        print(
            f"\nA total of {self._file_copied_count.__str__()} files have been created "
            f"and {self._file_skip_count.__str__()} files have been skipped."
        )


# This class is used to import the FBX files.
class TaskImportFBXs:
    """
    Import model task.
    """

    def __init__(self, _mapped_path_completed_dict: dict):
        self._mapped_path_completed_dict = _mapped_path_completed_dict
        self._source_group = None
        self._fbx_imported_count = 0
        self._fbx_import_fail_count = 0

    # This function is used to show the progress information.
    @staticmethod
    def show_progress_info_with_message(timer, progressbar, current, total):
        """
        :param timer:
        :param progressbar:
        :param current:
        :param total:
        """
        progressbar(current, total)
        timer(math.floor(current / total * 100))

    @staticmethod
    def func_handle_string_attr_to_object(prefix: str, attributes: dict, obj: str):
        """
        Handle string attribute to object.
        :param prefix: The prefix to add to the attribute.
        :param attributes: The attributes to add to the object.
        :param obj: The object to add the attributes to.
        """
        add_string_attr_to_object(prefix, attributes, obj)
        set_string_attr_to_object(prefix, attributes, obj)

    def task__create_groups(self):
        """
        Create groups.
        :return:
        """
        self._source_group = cmds.group(empty=True, name="source_gp")

    def task__import_fbx(self):
        """
        Import FBX.
        :return: The root node.
        """
        timer = TimeRecorder()
        progressbar = ProgressBar()
        for current, (filename, filepaths) in enumerate(
            self._mapped_path_completed_dict.items()
        ):
            filepath = filepaths[2]
            print(f"Importing {filepath}...")
            try:
                maya_object = import_model(filepath)
                cmds.parent(maya_object, self._source_group)
                self._fbx_imported_count += 1
            except Exception as e:
                self._fbx_import_fail_count += 1
                cmds.warning(f"Failed to import {filepath}, error: {e}")
            self.show_progress_info_with_message(
                timer, progressbar, current + 1, len(self._mapped_path_completed_dict)
            )

    def execute_tasks(self):
        """
        This function executes the tasks.
        """
        print("Creating groups...")
        self.task__create_groups()

        print("\nImporting FBXs...")
        self.task__import_fbx()

        print("All tasks completed successfully!")


def op_import_resources(self):
    tools.Log.import_resources_logger().info("Importing resources...")

    import_resources(self)


def import_resources(self):
    # Execute the task of collecting the FBXs.
    task_collect_fbx = TaskCollectFBXs(
        tools.Registry.get_value(reg_.REG_KEY, reg_.REG_SUB, reg_.REG_PROJ_DIR, ""),
        storage.ResourcesData.props["models_paths_mapping_by_type"],
    )
    task_collect_fbx.execute_tasks()

    # Execute the task of importing the FBXs.
    task_import_fbx = TaskImportFBXs(
        task_collect_fbx.func__get_mapped_path_completed_dict()
    )
    task_import_fbx.execute_tasks()

    # Execute the task of syncing the XML nodes.
    task_sync_xml_nodes = TaskSyncXMLNodes(storage.XMLData.root)
    task_sync_xml_nodes.execute_tasks()

    self.import_res_btn.set_force_visible(False)
    self.res_import_box.set_force_visible(False)
    tools.Log.import_resources_logger().info(
        "Completed importing resources, please check the script editor for more information"
    )

    construct_ui(self)


def construct_ui(self):
    # p = self.parse
    self.dynamic_ui.add_group(id="匯入結果", widget=qt.QtGroupVBoxCSWidget(text="匯入結果"))
    self.dynamic_ui.add_widget(
        parent_id="匯入結果",
        id="剩餘的錯誤數量提示",
        widget=qt.QtInfoBoxCSWidget(
            text=f"已完成匯入資源，請檢查腳本編輯器以獲取更多資訊。",
            status=qt.QtInfoBoxStatus.Success,
        ),
    )
    tools.Log.gui_logger().info("Completed constructing dynamic ui group manager")
