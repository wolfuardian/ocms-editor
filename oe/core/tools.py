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
class Maya:
    def browser(cls, file_mode, default_dir, file_filter): pass
    def get_main_window(cls): pass
    def decode_utf8_string(cls, byte_string): pass
    def decode_fbxasc_string(cls, fbxasc_string): pass
    def uuid(cls, node: str) -> str: pass

@interface
class Registry:
    def create_key(cls, key_name, subkey_name): pass
    def set_value(cls, key_name, subkey_name, val_name, val_data, val_type): pass
    def get_value(cls, key_name, subkey_name, value_name, default): pass
    def create_subkey(cls, key_name, subkey_name): pass
    def delete_subkey(cls, key_name, subkey_name): pass

@interface
class Logging:
    def installer_logger(cls): pass
    def registry_logger(cls): pass
    def fileio_logger(cls): pass
    def maya_logger(cls): pass
    def gui_logger(cls): pass
    def packages_logger(cls): pass
    def storage_logger(cls): pass
    def parse_xml_logger(cls): pass
    def parse_resources_logger(cls): pass

@interface
class Packages:
    def reload(cls, packages): pass
    def upload(cls, packages): pass

@interface
class Dictionary:
    def create_dict_from_lists(cls, key, val): pass

@interface
class IO:
    def read_utf16(cls, path): pass
    def convert_to_unix_path(cls, path): pass
    def convert_paths_to_unix_style(cls, paths): pass
    def list_filtered_paths(cls, directory, extension, re_pattern, recursive): pass
    def sort_files_by_size(cls, paths, is_reverse, is_dict): pass
    def get_maxsize_file(cls, paths): pass
    def get_minsize_file(cls, paths): pass
    def bytes_to_readable_size(cls, paths, is_reverse, is_dict): pass

@interface
class XML:
    def root(cls, xmlstring): pass
    def iterator(cls, root, tag, attr, kwd): pass
    def enumerator(cls, elems, attr, mode, out_attr, test_print): pass
    def extractor(cls, elems, pos_attrs, neg_attrs, pos_op, neg_op): pass
    def collect_attrs(cls, elems, kwd): pass
    def collect_unique_attrs(cls, root): pass

@interface
class String:
    def list_to_string(cls, lst): pass
    def dict_to_string(cls, dictionary): pass
# fmt: on
