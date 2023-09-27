import os
import re

from maya import cmds

xml_data = {
    "root|inventec-smart-factory": {
        "global": {
            "index": "1",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Building-inventec-smart-factory-0001",
            "parent": "",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory",
            "parent": "root",
            "element": "<Element 'Object' at 0x000001E9B33A4450>",
            "deep": "1",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Building",
            "category": "0",
            "name": "inventec-smart-factory",
            "alias": "\u82f1\u696d\u9054\u667a\u6167\u5de5\u5ee0",
            "model": "inventec-smart-factory",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "",
            "id": "",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "0", "y": "0", "z": "0"},
            "rotation": {"x": "-0", "y": "90", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '30.00003'}, {'name': 'yaw', 'text': '-90'}, {'name': 'zoom', 'text': '119'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "True",
            "is_none": "False",
            "is_temp": "True",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": "inventec-smart-factory"},
    },
    "root|inventec-smart-factory|Inventec_Production_line": {
        "global": {
            "index": "2",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Room--0002",
            "parent": "OCMS-Building-inventec-smart-factory-0001",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line",
            "parent": "root|inventec-smart-factory",
            "element": "<Element 'Object' at 0x000001E9B33A48B0>",
            "deep": "2",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Room",
            "category": "0",
            "name": "Inventec_Production_line",
            "alias": "L41",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "2.178143", "y": "0.224962533", "z": "-14.25829"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '30.00001'}, {'name': 'yaw', 'text': '-90'}, {'name': 'zoom', 'text': '32'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "True",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A": {
        "global": {
            "index": "3",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Room--0003",
            "parent": "OCMS-Room--0002",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A",
            "parent": "root|inventec-smart-factory|Inventec_Production_line",
            "element": "<Element 'Object' at 0x000001E9B33A4E50>",
            "deep": "3",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Room",
            "category": "0",
            "name": "Inventec_Production_line_A",
            "alias": "A\u5340",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "-1.9136523", "y": "0.00209438312", "z": "8.567537"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '30.00001'}, {'name': 'yaw', 'text': '-90'}, {'name': 'zoom', 'text': '44'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "True",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Staff_03": {
        "global": {
            "index": "4",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device--0004",
            "parent": "OCMS-Room--0003",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Staff_03",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A",
            "element": "<Element 'Object' at 0x000001E9B33B2590>",
            "deep": "4",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "Staff_03",
            "alias": "\u6295\u5165\u7ad9",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "L41_01",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "-34.02469", "y": "-0.00282018655", "z": "-0.6298773"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '60.00003'}, {'name': 'yaw', 'text': '-90.14183'}, {'name': 'zoom', 'text': '9'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|solderprinter_01": {
        "global": {
            "index": "5",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device--0005",
            "parent": "OCMS-Room--0003",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|solderprinter_01",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A",
            "element": "<Element 'Object' at 0x000001E9B33B2D10>",
            "deep": "4",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "solderprinter_01",
            "alias": "\u5370\u5237\u6a5fB",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "L41_02",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "-32.4737473", "y": "-0.00509389862", "z": "-0.3076503"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '60.00002'}, {'name': 'yaw', 'text': '-90'}, {'name': 'zoom', 'text': '8'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Solder_Paste_Inspection_05": {
        "global": {
            "index": "6",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device--0006",
            "parent": "OCMS-Room--0003",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Solder_Paste_Inspection_05",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A",
            "element": "<Element 'Object' at 0x000001E9B33B54F0>",
            "deep": "4",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "Solder_Paste_Inspection_05",
            "alias": "\u932b\u818f\u6aa2\u6e2c\u6a5fB",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "L41_03",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {
                "x": "-30.4927044",
                "y": "-0.00509391772",
                "z": "-0.510306358",
            },
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '60.00002'}, {'name': 'yaw', 'text': '-90'}, {'name': 'zoom', 'text': '9'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Pick_Place_Machine_A": {
        "global": {
            "index": "7",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device--0007",
            "parent": "OCMS-Room--0003",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Pick_Place_Machine_A",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A",
            "element": "<Element 'Object' at 0x000001E9B33B5C70>",
            "deep": "4",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "Pick_Place_Machine_A",
            "alias": "\u7f6e\u4ef6\u6a5fB",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "L41_04",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "-26.81232", "y": "-3.433227E-07", "z": "-0.3814822"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '60.00002'}, {'name': 'yaw', 'text': '-90'}, {'name': 'zoom', 'text': '9'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Reflow_01": {
        "global": {
            "index": "8",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device--0008",
            "parent": "OCMS-Room--0003",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Reflow_01",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A",
            "element": "<Element 'Object' at 0x000001E9B33B7400>",
            "deep": "4",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "Reflow_01",
            "alias": "\u8ff4\u710a\u7210B",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "L41_05",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "-19.7562561", "y": "-0.00419216137", "z": "-0.5003406"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '60.00002'}, {'name': 'yaw', 'text': '-90'}, {'name': 'zoom', 'text': '9'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Solder_Paste_Inspection_04": {
        "global": {
            "index": "9",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device--0009",
            "parent": "OCMS-Room--0003",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Solder_Paste_Inspection_04",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A",
            "element": "<Element 'Object' at 0x000001E9B33B7B80>",
            "deep": "4",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "Solder_Paste_Inspection_04",
            "alias": "SMT\u81ea\u52d5\u5149\u5b78\u6aa2\u67e5\u6a5fB",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "L41_06",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "-12.8878584", "y": "0.006655006", "z": "-0.5103063"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '60.00002'}, {'name': 'yaw', 'text': '-90'}, {'name': 'zoom', 'text': '7'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Solder_Printer_02": {
        "global": {
            "index": "10",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device--0010",
            "parent": "OCMS-Room--0003",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Solder_Printer_02",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A",
            "element": "<Element 'Object' at 0x000001E9B33BC360>",
            "deep": "4",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "Solder_Printer_02",
            "alias": "\u5370\u5237\u6a5fA",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "L41_07",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "-8.763092", "y": "-0.00509389862", "z": "-0.6319898"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '60'}, {'name': 'yaw', 'text': '-90'}, {'name': 'zoom', 'text': '7'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Solder_Paste_Inspection_03": {
        "global": {
            "index": "11",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device--0011",
            "parent": "OCMS-Room--0003",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Solder_Paste_Inspection_03",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A",
            "element": "<Element 'Object' at 0x000001E9B33BCAE0>",
            "deep": "4",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "Solder_Paste_Inspection_03",
            "alias": "\u932b\u818f\u6aa2\u6e2c\u6a5fA",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "L41_08",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "-6.8700366", "y": "0.006655006", "z": "-0.5103063"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '60'}, {'name': 'yaw', 'text': '-90'}, {'name': 'zoom', 'text': '9'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Pick_Place_Machine_B": {
        "global": {
            "index": "12",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device--0012",
            "parent": "OCMS-Room--0003",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Pick_Place_Machine_B",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A",
            "element": "<Element 'Object' at 0x000001E9B33BF2C0>",
            "deep": "4",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "Pick_Place_Machine_B",
            "alias": "\u7f6e\u4ef6\u6a5fA",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "L41_09",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "-3.179802", "y": "-3.433227E-07", "z": "-0.3814822"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '60.00002'}, {'name': 'yaw', 'text': '-90'}, {'name': 'zoom', 'text': '9'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Reflow02": {
        "global": {
            "index": "13",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device--0013",
            "parent": "OCMS-Room--0003",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Reflow02",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A",
            "element": "<Element 'Object' at 0x000001E9B33BF9F0>",
            "deep": "4",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "Reflow02",
            "alias": "\u8ff4\u710a\u7210A",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "L41_10",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "4.09869671", "y": "-0.004053154", "z": "-0.735375643"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '60.00002'}, {'name': 'yaw', 'text': '-90'}, {'name': 'zoom', 'text': '9'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Solder_Paste_Inspection3": {
        "global": {
            "index": "14",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device--0014",
            "parent": "OCMS-Room--0003",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Solder_Paste_Inspection3",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A",
            "element": "<Element 'Object' at 0x000001E9B33C31D0>",
            "deep": "4",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "Solder_Paste_Inspection3",
            "alias": "SMT\u81ea\u52d5\u5149\u5b78\u6aa2\u67e5\u6a5fA",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "L41_11",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "11.4976044", "y": "0.006655006", "z": "-0.5103063"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '60.00002'}, {'name': 'yaw', 'text': '-90'}, {'name': 'zoom', 'text': '7'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Insertion_a": {
        "global": {
            "index": "15",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device--0015",
            "parent": "OCMS-Room--0003",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Insertion_a",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A",
            "element": "<Element 'Object' at 0x000001E9B33C3900>",
            "deep": "4",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "Insertion_a",
            "alias": "\u88dd\u63d2\u7ad9",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "16.9226055", "y": "-0.004257946", "z": "-0.5316171"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '29.98189'}, {'name': 'yaw', 'text': '90.08698'}, {'name': 'zoom', 'text': '7'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|JET_7300TBII_BP": {
        "global": {
            "index": "16",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device--0016",
            "parent": "OCMS-Room--0003",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|JET_7300TBII_BP",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A",
            "element": "<Element 'Object' at 0x000001E9B33C6090>",
            "deep": "4",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "JET_7300TBII_BP",
            "alias": "HI\u81ea\u52d5\u5149\u5b78\u6aa2\u67e5\u6a5f",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "L41_13",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "19.7158489", "y": "-0.004192153", "z": "-0.5546695"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '40'}, {'name': 'yaw', 'text': '90.02346'}, {'name': 'zoom', 'text': '8'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Wave_Solder_a": {
        "global": {
            "index": "17",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device--0017",
            "parent": "OCMS-Room--0003",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|Wave_Solder_a",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A",
            "element": "<Element 'Object' at 0x000001E9B33C67C0>",
            "deep": "4",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "Wave_Solder_a",
            "alias": "\u6ce2\u5cf0\u710a",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "L41_14",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "25.6746788", "y": "0.0541500449", "z": "-0.4281326"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '60'}, {'name': 'yaw', 'text': '90.02843'}, {'name': 'zoom', 'text': '8'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|X_ray_Inspection": {
        "global": {
            "index": "18",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device--0018",
            "parent": "OCMS-Room--0003",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|X_ray_Inspection",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A",
            "element": "<Element 'Object' at 0x000001E9B33C6F40>",
            "deep": "4",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "X_ray_Inspection",
            "alias": "3D X-ray",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "L41_15",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "37.07638", "y": "-0.0152550312", "z": "-1.59354973"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '26.35267'}, {'name': 'yaw', 'text': '152.4478'}, {'name': 'zoom', 'text': '7'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|\u76e3\u63a7": {
        "global": {
            "index": "19",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Room--0019",
            "parent": "OCMS-Room--0003",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|\u76e3\u63a7",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A",
            "element": "<Element 'Object' at 0x000001E9B33CA6D0>",
            "deep": "4",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Room",
            "category": "0",
            "name": "\u76e3\u63a7",
            "alias": "",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "",
            "id": "",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "0", "y": "0", "z": "0"},
            "rotation": {"x": "-0", "y": "270", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {"Component": "[]", "is_dirty": "<Not yet resolved>"},
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "True",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|\u76e3\u63a7|CCTV_1": {
        "global": {
            "index": "20",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device-device-nvr-nvr003-0020",
            "parent": "OCMS-Room--0019",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|\u76e3\u63a7|CCTV_1",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|\u76e3\u63a7",
            "element": "<Element 'Object' at 0x000001E9B33CAAE0>",
            "deep": "5",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "CCTV_1",
            "alias": "",
            "model": "device/nvr/nvr003",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "",
            "id": "",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "-2.86408019", "y": "4.47515249", "z": "26.6747646"},
            "rotation": {"x": "40.00001", "y": "90", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Diagram.CCTV', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'm_videoPath', 'text': 'rtsp://admin:Cctv1234@10.6.180.33:1034/stream0'}, {'name': 'm_isFixedAspectRatio', 'text': 'True'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "True",
            "is_none": "False",
            "is_temp": "True",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": "device/nvr/nvr003"},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|\u76e3\u63a7|CCTV_2": {
        "global": {
            "index": "21",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device-device-nvr-nvr003-0021",
            "parent": "OCMS-Room--0019",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|\u76e3\u63a7|CCTV_2",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|\u76e3\u63a7",
            "element": "<Element 'Object' at 0x000001E9B33CD270>",
            "deep": "5",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "CCTV_2",
            "alias": "",
            "model": "device/nvr/nvr003",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "",
            "id": "",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "-2.86", "y": "4.47515249", "z": "2.85541058"},
            "rotation": {"x": "40.00001", "y": "90", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Diagram.CCTV', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'm_videoPath', 'text': 'rtsp://admin:Cctv1234@10.6.180.33:1032/stream0'}, {'name': 'm_isFixedAspectRatio', 'text': 'True'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "True",
            "is_none": "False",
            "is_temp": "True",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": "device/nvr/nvr003"},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|\u76e3\u63a7|CCTV_3": {
        "global": {
            "index": "22",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device-device-nvr-nvr003-0022",
            "parent": "OCMS-Room--0019",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|\u76e3\u63a7|CCTV_3",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|\u76e3\u63a7",
            "element": "<Element 'Object' at 0x000001E9B33CD9A0>",
            "deep": "5",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "CCTV_3",
            "alias": "",
            "model": "device/nvr/nvr003",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "",
            "id": "",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "-5.07764244", "y": "4.47515249", "z": "-25.6870937"},
            "rotation": {"x": "15.00003", "y": "335", "z": "-1.10486451E-06"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Diagram.CCTV', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'm_videoPath', 'text': 'rtsp://admin:Cctv1234@10.6.180.33:1028/stream0'}, {'name': 'm_isFixedAspectRatio', 'text': 'True'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "True",
            "is_none": "False",
            "is_temp": "True",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": "device/nvr/nvr003"},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|\u76e3\u63a7|CCTV_4": {
        "global": {
            "index": "23",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device-device-nvr-nvr001-0023",
            "parent": "OCMS-Room--0019",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|\u76e3\u63a7|CCTV_4",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|\u76e3\u63a7",
            "element": "<Element 'Object' at 0x000001E9B33D0130>",
            "deep": "5",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "CCTV_4",
            "alias": "",
            "model": "device/nvr/nvr001",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "",
            "id": "",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "0.9889475", "y": "4.868341", "z": "8.912336"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Diagram.CCTV', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'm_videoPath', 'text': 'rtsp://admin:1234@10.6.180.33:1036/stream1'}, {'name': 'm_isFixedAspectRatio', 'text': 'True'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "True",
            "is_none": "False",
            "is_temp": "True",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": "device/nvr/nvr001"},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|\u76e3\u63a7|CCTV_5": {
        "global": {
            "index": "25",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device-device-nvr-nvr003-0025",
            "parent": "OCMS-Room--0019",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|\u76e3\u63a7|CCTV_5",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|\u76e3\u63a7",
            "element": "<Element 'Object' at 0x000001E9B33D0F90>",
            "deep": "5",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "CCTV_5",
            "alias": "",
            "model": "device/nvr/nvr003",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "",
            "id": "",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "-0.438603461", "y": "2.13115835", "z": "-32.5208626"},
            "rotation": {"x": "90", "y": "270", "z": "0"},
            "scale": {"x": "0.499999881", "y": "0.499999881", "z": "0.5"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Diagram.CCTV', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'm_isFixedAspectRatio', 'text': 'True'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "True",
            "is_none": "False",
            "is_temp": "True",
            "is_dupe": "True",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": "device/nvr/nvr003"},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|5G Private Network": {
        "global": {
            "index": "26",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Unknown--0026",
            "parent": "OCMS-Room--0003",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|5G Private Network",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A",
            "element": "<Element 'Object' at 0x000001E9B33D46D0>",
            "deep": "4",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Unknown",
            "category": "0",
            "name": "5G Private Network",
            "alias": "",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "",
            "id": "",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "-0.264492631", "y": "-0.22705698", "z": "5.68975735"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {"Component": "[]", "is_dirty": "<Not yet resolved>"},
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "True",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|5G Private Network|RU01": {
        "global": {
            "index": "27",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device-device-inventec-ru-0027",
            "parent": "OCMS-Unknown--0026",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|5G Private Network|RU01",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|5G Private Network",
            "element": "<Element 'Object' at 0x000001E9B33D4AE0>",
            "deep": "5",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "RU01",
            "alias": "",
            "model": "device/inventec-ru",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "",
            "id": "RU_01",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "13.9127817", "y": "3.997925", "z": "-6.05442238"},
            "rotation": {"x": "-0", "y": "270", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '30'}, {'name': 'zoom', 'text': '4'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "True",
            "is_none": "False",
            "is_temp": "True",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": "device/inventec-ru"},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|5G Private Network|RU02": {
        "global": {
            "index": "28",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device-device-inventec-ru-0028",
            "parent": "OCMS-Unknown--0026",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|5G Private Network|RU02",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|5G Private Network",
            "element": "<Element 'Object' at 0x000001E9B3334E50>",
            "deep": "5",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "RU02",
            "alias": "",
            "model": "device/inventec-ru",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "",
            "id": "RU_02",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "-5.074319", "y": "4", "z": "-5.45957661"},
            "rotation": {"x": "-0", "y": "270", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '30'}, {'name': 'zoom', 'text': '4'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "True",
            "is_none": "False",
            "is_temp": "True",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": "device/inventec-ru"},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|5G Private Network|RU03": {
        "global": {
            "index": "29",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device-device-inventec-ru-0029",
            "parent": "OCMS-Unknown--0026",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|5G Private Network|RU03",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|5G Private Network",
            "element": "<Element 'Object' at 0x000001E9B033A4A0>",
            "deep": "5",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "RU03",
            "alias": "",
            "model": "device/inventec-ru",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "",
            "id": "RU_03",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "-25.0472546", "y": "4", "z": "-5.7094574"},
            "rotation": {"x": "-0", "y": "270", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '30'}, {'name': 'zoom', 'text': '4'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "True",
            "is_none": "False",
            "is_temp": "True",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": "device/inventec-ru"},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|5G Private Network|CPE01": {
        "global": {
            "index": "30",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Device-device-inventec-cpe-0030",
            "parent": "OCMS-Unknown--0026",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|5G Private Network|CPE01",
            "parent": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_A|5G Private Network",
            "element": "<Element 'Object' at 0x000001E9B033A8B0>",
            "deep": "5",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Device",
            "category": "0",
            "name": "CPE01",
            "alias": "",
            "model": "device/inventec-cpe",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "",
            "id": "CPE_01",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "19.68534", "y": "4", "z": "-5.637064"},
            "rotation": {"x": "-0", "y": "270", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '30'}, {'name': 'zoom', 'text': '4'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "True",
            "is_none": "False",
            "is_temp": "True",
            "is_dupe": "False",
            "is_non_device": "False",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": "device/inventec-cpe"},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_B": {
        "global": {
            "index": "31",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Room--0031",
            "parent": "OCMS-Room--0002",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_B",
            "parent": "root|inventec-smart-factory|Inventec_Production_line",
            "element": "<Element 'Object' at 0x000001E9B0311450>",
            "deep": "3",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Room",
            "category": "0",
            "name": "Inventec_Production_line_B",
            "alias": "B\u5340",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "-12.0401564", "y": "-0.00341732", "z": "-3.92340875"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '46.24675'}, {'name': 'yaw', 'text': '-88.72009'}, {'name': 'zoom', 'text': '18'}, {'name': 'offset', 'text': '{\"x\":0.1905956268310547,\"y\":-0.5378469228744507,\"z\":0.3691835403442383}'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "True",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_C": {
        "global": {
            "index": "32",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Room--0032",
            "parent": "OCMS-Room--0002",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line|Inventec_Production_line_C",
            "parent": "root|inventec-smart-factory|Inventec_Production_line",
            "element": "<Element 'Object' at 0x000001E9B030C950>",
            "deep": "3",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Room",
            "category": "0",
            "name": "Inventec_Production_line_C",
            "alias": "C\u5340",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "static",
            "id": "",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "16.34363", "y": "-0.0132973194", "z": "-2.69503117"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '44.54755'}, {'name': 'yaw', 'text': '-90.23492'}, {'name': 'zoom', 'text': '15'}, {'name': 'offset', 'text': '{\"x\":0.7475166320800781,\"y\":-0.7557405829429627,\"z\":-0.5649337768554688}'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "True",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Build": {
        "global": {
            "index": "33",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Room--0033",
            "parent": "OCMS-Building-inventec-smart-factory-0001",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Build",
            "parent": "root|inventec-smart-factory",
            "element": "<Element 'Object' at 0x000001E9A65DCC20>",
            "deep": "2",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Room",
            "category": "0",
            "name": "Inventec_Build",
            "alias": "\u5ee0\u5340",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "hide|static",
            "id": "",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "5.20624447", "y": "0", "z": "-0.931184232"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {
            "Component": "[{'name': 'OCMS.Scene.FocusAt', 'assembly': 'Nadi.OCMS', 'property': [{'name': 'pitch', 'text': '30.00001'}, {'name': 'yaw', 'text': '-90'}, {'name': 'zoom', 'text': '119'}]}]",
            "is_dirty": "<Not yet resolved>",
        },
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "True",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line_L42": {
        "global": {
            "index": "34",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Room--0034",
            "parent": "OCMS-Building-inventec-smart-factory-0001",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line_L42",
            "parent": "root|inventec-smart-factory",
            "element": "<Element 'Object' at 0x000001E9A65DC360>",
            "deep": "2",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Room",
            "category": "0",
            "name": "Inventec_Production_line_L42",
            "alias": "Inventec_Production_line_L42",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "hide|static",
            "id": "",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "2.178143", "y": "0.224962533", "z": "-5"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {"Component": "[]", "is_dirty": "<Not yet resolved>"},
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "True",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line_L43": {
        "global": {
            "index": "35",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Room--0035",
            "parent": "OCMS-Building-inventec-smart-factory-0001",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line_L43",
            "parent": "root|inventec-smart-factory",
            "element": "<Element 'Object' at 0x000001E9A65DC040>",
            "deep": "2",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Room",
            "category": "0",
            "name": "Inventec_Production_line_L43",
            "alias": "Inventec_Production_line_L43",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "hide|static",
            "id": "",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "2.178143", "y": "0.224962533", "z": "5.9"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {"Component": "[]", "is_dirty": "<Not yet resolved>"},
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "True",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
    "root|inventec-smart-factory|Inventec_Production_line_L44": {
        "global": {
            "index": "36",
            "product_type": "OCMS2_0",
            "is_dirty": "<Not yet resolved>",
        },
        "maya": {
            "uuid": "OCMS-Room--0036",
            "parent": "OCMS-Building-inventec-smart-factory-0001",
            "is_synced_attribute": "<Not yet resolved>",
            "is_synced_resource": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "element_tree": {
            "path": "root|inventec-smart-factory|Inventec_Production_line_L44",
            "parent": "root|inventec-smart-factory",
            "element": "<Element 'Object' at 0x000001E9A65281D0>",
            "deep": "2",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {
            "type": "Room",
            "category": "0",
            "name": "Inventec_Production_line_L44",
            "alias": "Inventec_Production_line_L44",
            "model": "",
            "bundle": "",
            "time": "2023/02/16 10:29",
            "noted": "modified",
            "remark": "hide|static",
            "id": "",
            "is_dirty": "<Not yet resolved>",
        },
        "transform": {
            "position": {"x": "2.178143", "y": "0.224962533", "z": "17.5"},
            "rotation": {"x": "0", "y": "0", "z": "0"},
            "scale": {"x": "1", "y": "1", "z": "1"},
            "is_dirty": "<Not yet resolved>",
        },
        "component": {"Component": "[]", "is_dirty": "<Not yet resolved>"},
        "parser": {
            "is_okay": "False",
            "is_none": "True",
            "is_temp": "False",
            "is_dupe": "False",
            "is_non_device": "True",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "<Not yet resolved>",
            "size": "<Not yet resolved>",
            "copy_to_path": "<Not yet resolved>",
            "is_dirty": "<Not yet resolved>",
        },
        "resource": {"model": ""},
    },
}


res_data = {
    "device/inventec-cpe": {
        "global": {
            "index": "1",
            "project_path": "C:/Users/eos/OCMSProject",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "C:/Users/eos/OCMSProject/resources/inventec-cpe.fbx",
            "size": "70768",
            "copy_to_path": "C:/Users/eos/OCMSProject/inventec-cpe/inventec-cpe.fbx",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {"model": "device/inventec-cpe", "is_dirty": "<Not yet resolved>"},
    },
    "device/inventec-ru": {
        "global": {
            "index": "2",
            "project_path": "C:/Users/eos/OCMSProject",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "C:/Users/eos/OCMSProject/resources/inventec-ru.fbx",
            "size": "31616",
            "copy_to_path": "C:/Users/eos/OCMSProject/inventec-ru/inventec-ru.fbx",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {"model": "device/inventec-ru", "is_dirty": "<Not yet resolved>"},
    },
    "device/nvr/nvr001": {
        "global": {
            "index": "4",
            "project_path": "C:/Users/eos/OCMSProject",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "C:/Users/eos/OCMSProject/resources/NVR001.fbx",
            "size": "57072",
            "copy_to_path": "C:/Users/eos/OCMSProject/nvr001/nvr001.fbx",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {"model": "device/nvr/nvr001", "is_dirty": "<Not yet resolved>"},
    },
    "device/nvr/nvr003": {
        "global": {
            "index": "5",
            "project_path": "C:/Users/eos/OCMSProject",
            "is_dirty": "<Not yet resolved>",
        },
        "file": {
            "path": "C:/Users/eos/OCMSProject/resources/NVR003.fbx",
            "size": "161360",
            "copy_to_path": "C:/Users/eos/OCMSProject/nvr003/nvr003.fbx",
            "is_dirty": "<Not yet resolved>",
        },
        "object": {"model": "device/nvr/nvr003", "is_dirty": "<Not yet resolved>"},
    },
}


def to_underscore(name):
    return re.sub(r"\W+", lambda match: "_" * len(match.group()), name)


def extract_filename(path):
    return os.path.splitext(os.path.basename(path))[0]


def add_group(obj_name):
    group_name = cmds.group(empty=True, name=obj_name)
    if group_name != obj_name:
        cmds.delete(group_name)
        group_name = cmds.rename(group_name, obj_name)

    return group_name


def import_file(path, type="FBX"):
    return cmds.file(
        path,
        i=True,
        force=True,
        type=type,
        ignoreVersion=True,
        mergeNamespacesOnClash=True,
        returnNewNodes=True,
    )


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
            nice_name = add_attr.replace(attr_compound_name, "")
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


#
# path = r"C:\Users\eos\OCMSProject\resources\Sever008.fbx".replace("\\", "/")
#
#
# model_name = extract_filename(path).lower()
# group_name = f"i_{model_name}_gp"
# group = cmds.group(empty=True, name=group_name)
#
# if group != group_name:
#     cmds.delete(group_name)
#     group = cmds.rename(group, group_name)
#


class ModelImporter:
    def execute(self):
        self.add_groups()
        self.add_model_to_scene()
        self.hide_group()

    def add_groups(self):
        for model, data in res_data.items():
            filepath = data["file"]["path"]
            group_name = to_underscore(extract_filename(filepath)).lower()
            new_group = add_group(f"r_{group_name}")
            res_data[model].setdefault("maya", {})
            res_data[model]["maya"]["raw_model"] = new_group

    def add_model_to_scene(self):
        for model, data in res_data.items():
            group_name = res_data[model]["maya"]["raw_model"]
            new_objects = import_file(data["file"]["path"])
            children = cmds.parent(new_objects, group_name)
            res_data[model].setdefault("maya", {})
            res_data[model]["maya"]["children"] = children

    def hide_group(self):
        for model, data in res_data.items():
            group_name = res_data[model]["maya"]["raw_model"]
            cmds.hide(group_name)


class OCMSDataSyncHandler:
    def execute(self):
        self.add_groups()
        self.set_parent()
        self.copy_model_to_node()
        self.add_system_attributes()
        self.apply_transform()

    def add_groups(self):
        for xpath, data in xml_data.items():
            object_name = data["maya"]["uuid"]
            group_name = to_underscore(object_name)
            new_group = add_group(group_name)

    def set_parent(self):
        for xpath, data in xml_data.items():
            object_unique_name = data["maya"]["uuid"]
            object_parent_name = data["maya"]["parent"]
            group_name = to_underscore(object_unique_name)
            parent_group_name = to_underscore(object_parent_name)
            if parent_group_name == "":
                continue
            children = cmds.parent(group_name, parent_group_name)

    def copy_model_to_node(self):
        for xpath, data in xml_data.items():
            model_name = data["resource"]["model"]
            if model_name in res_data.keys():
                node_name = to_underscore(data["maya"]["uuid"])
                instance_group = res_data[model_name]["maya"]["raw_model"]
                # duplicate_group = cmds.duplicate(instance_group, rr=True)[0]

                # cmds.setAttr(f"{duplicate_group}.scaleX", 1)
                # cmds.setAttr(f"{duplicate_group}.scaleY", 1)
                # cmds.setAttr(f"{duplicate_group}.scaleZ", 1)

                # duplicate_group = cmds.spaceLocator()
                # cmds.showHidden(duplicate_group)
                target_group = node_name
                # cmds.parent(duplicate_group, target_group)
                # cmds.rename(duplicate_group, f"inst_{node_name}")

                new_locator = cmds.spaceLocator(name=f"l_{model}")
                cmds.parent(new_locator, target_group)

    def add_system_attributes(self):
        _system_attributes = []
        for xpath, data in xml_data.items():
            # Global
            index = data["global"]["index"]
            product = data["global"]["product_type"]

            compound_name = "Global"
            attrs = {
                compound_name + "index": index,
                compound_name + "product": product,
            }
            node_name = to_underscore(data["maya"]["uuid"])

            add_string_attr_to_object(compound_name, attrs, node_name)
            set_string_attr_to_object(compound_name, attrs, node_name)

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
                compound_name + "type": index,
                compound_name + "product": product,
                compound_name + "category": category,
                compound_name + "name": name,
                compound_name + "alias": alias,
                compound_name + "model": model,
                compound_name + "bundle": bundle,
                compound_name + "time": time,
                compound_name + "noted": noted,
                compound_name + "remark": remark,
                compound_name + "id": id,
            }
            node_name = to_underscore(data["maya"]["uuid"])

            add_string_attr_to_object(compound_name, attrs, node_name)
            set_string_attr_to_object(compound_name, attrs, node_name)

            aaa = (
                {
                    "Component": [
                        {
                            "name": "OCMS.Diagram.CCTV",
                            "assembly": "Nadi.OCMS",
                            "property": [
                                {
                                    "name": "m_videoPath",
                                    "text": "rtsp://admin:Cctv1234@10.6.180.33:1028/stream0",
                                },
                                {
                                    "name": "m_isFixedAspectRatio",
                                    "text": "True"
                                },
                            ],
                        },
                        {
                            "name": "NADILeanTouch.LeanCameraSettingValue",
                            "assembly": "Nadi.OCMS",
                            "property": [
                                {
                                    "name": "m_videoPath",
                                    "text": "rtsp://admin:Cctv1234@10.6.180.33:1028/stream0",
                                },
                                {"name": "m_isFixedAspectRatio", "text": "True"},
                            ],
                        },
                        {
                            "name": "NADIRealDataUIList.Realtime2DTemplate04",
                            "assembly": "Nadi.OCMS",
                            "property": [
                                {
                                    "name": "m_videoPath",
                                    "text": "rtsp://admin:Cctv1234@10.6.180.33:1028/stream0",
                                },
                                {"name": "m_isFixedAspectRatio", "text": "True"},
                            ],
                        },
                    ],
                    "is_dirty": "<Not yet resolved>",
                },
            )

            # Component
            component = data["global"]["component"]
            # for _, data in component.items():

            # component_lst = component
            # compound_name = "Component"

            compound_name = "Global"
            attrs = {
                compound_name + "index": index,
                compound_name + "product": product,
            }
            node_name = to_underscore(data["maya"]["uuid"])

            add_string_attr_to_object(compound_name, attrs, node_name)
            set_string_attr_to_object(compound_name, attrs, node_name)

    def apply_transform(self):
        for xpath, data in xml_data.items():
            object_name = to_underscore(data["maya"]["uuid"])
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


mi = ModelImporter()
mi.execute()

osh = OCMSDataSyncHandler()
osh.execute()


# log
for model, data in res_data.items():
    for k, v in data.items():
        if k == "maya":
            print(f"model: {model}")
            string = ""
            for attr in v:
                string += f"{attr}: {v[attr]}\n"
            print(string)
