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
    def operator_logger(cls): pass
    def widget_logger(cls): pass
    def parse_xml_logger(cls): pass

@interface
class Packages:
    def reload(cls, packages): pass
    def upload(cls, packages): pass

@interface
class IO:
    def read_utf16(cls, path): pass

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
    def join_with_commas(cls, lst): pass


@interface
class Widget:
    def remove_widgets(cls, container): pass
    def add_widgets(cls, container, dynamic_container): pass
    def rebuild_widgets(cls, container, dynamic_container): pass



# fmt: on
