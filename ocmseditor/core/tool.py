import abc
import inspect


# Note: The following implementation utilizes a portion of code from BlenderBIM. This inclusion is necessary due to
# certain technical challenges inherent in the problem that are adeptly addressed by the BlenderBIM's solution.
# The use of this code segment is not intended as a claim of originality, but rather as a testament to
# the efficacy of the adopted approach.
# fmt: off
class Interface(abc.ABC): pass


def interface(cls):
    attrs = {n: classmethod(abc.abstractmethod(f)) for n, f in inspect.getmembers(cls, predicate=inspect.isfunction)}
    return type(cls.__name__, (Interface, cls), attrs)
@interface
class Collect:
    def collect_attr_values(cls, datasheet, attr): pass
    def collect_sorted_files_by_size(cls, datasheet, reverse, readable): pass
@interface
class Debug:
    def print_beautiful_dictionary(cls, data, level, indent): pass
    def print_ocms_datasheet_dictionary(cls, ocms_datasheet, count, beauty, indent): pass
@interface
class Dictionary:
    def assemble(cls, keys, values): pass
    def slice(cls, dictionary, count): pass
    def flatten(cls, dictionary, level, indent): pass
    def convert_all_to_string(cls, dictionary): pass
    def write_to_json_style(cls, dictionary, path, indent): pass
@interface
class File:
    def exists(cls, path): pass
    def is_dir(cls, path): pass
    def is_file(cls, path): pass
    def is_xml(cls, path): pass
    def glob(cls, directory, extension, pattern, recursive): pass
    def read_utf16(cls, path): pass
    def get_size(cls, path): pass
    def get_project_path(cls): pass
    def get_copy_to_path(cls, path): pass
    def bytes_to_readable_size(cls, size_bytes, precision, unit): pass
    def split_basename_without_ext(cls, path): pass
    def open_on_explorer(cls, path): pass
@interface
class Maya:
    def get_main_window(cls): pass
    def browser(cls, file_mode, default_dir, file_filter): pass
    def import_file(cls, path, typ): pass
    def uuid(cls, obj_name): pass
    def get_selected(cls): pass
    def get_top_level_transforms(cls): pass
    def obj_exists(cls, obj_name): pass
    def attr_exists(cls, attr_name, obj_name): pass
    def add_compound_attr(cls, attr_name, child_count, obj_name): pass
    def add_string_child_attr(cls, attr_name, parent_attr_name, obj_name): pass
    def set_string_attr(cls, attr_name, attr_value, obj_name): pass
    def add_string_attr_to_obj(cls, attr_compound_name, attrs, obj_name): pass
    def set_string_attr_to_obj(cls, attr_compound_name, attrs, obj_name): pass
    def setup_string_attr_to_obj(cls, prefix, attrs, obj_name): pass
    def add_group(cls, obj_name): pass
    def select(cls, obj_name): pass
    def parent(cls, obj_name, parent_obj_name): pass
    def delete(cls, obj_name): pass
@interface
class Name:
    def to_underscore(cls, name): pass
@interface
class OCMS:
    def get_ocms(cls): pass
@interface
class Registry:
    def get_reg(cls, data_name, reserved, default): pass
    def set_reg(cls, data_name, data_value, reserved, data_type): pass
@interface
class String:
    def list_to_string(cls, lst): pass
    def dict_to_string(cls, dictionary): pass
    def decode_utf8_string(cls, byte_string): pass
    def decode_fbxasc_string(cls, fbxasc_string): pass
@interface
class UUID:
    def format_number_with_digits(cls, number, num_digits): pass
    def generate_ocms_uuid(cls, type_str, model, number): pass
@interface
class Widget:
    def disable(cls, widget): pass
    def enable(cls, widget): pass
    def show_hide(cls, widget, show): pass
    def set_text(cls, widget, text): pass
@interface
class XML:
    def all_attrs(cls, elem, attrs): pass
    def any_attrs(cls, elem, attrs): pass
    def enum_attrs(cls, elem): pass
    def enum_tags(cls, elem): pass
    def exclude_attrs(cls, elem, exclude_attrs, exclude_logic): pass
    def include_attrs(cls, elem, include_attrs, include_logic): pass
    def filter_elem(cls, elem, include_attrs, exclude_attrs, include_logic, exclude_logic): pass
    def extract_comp_attrs(cls, elem): pass
    def extract_xform_attrs(cls, elem): pass
    def get_attr(cls, elem, attr, out_attr): pass
    def query_elems_attrs(cls, elems, attr, out_attr): pass
    def iter_elems_paths(cls, elem, tag, root_path, separator): pass
    def parent_path(cls, path, separator, remove_num): pass
    def root(cls, doc): pass
# fmt: on
