import abc
import inspect


# Note: The following implementation utilizes a portion of code from BlenderBIM. This inclusion is necessary due to
# certain technical challenges inherent in the problem that are adeptly addressed by the BlenderBIM's solution.
# The use of this code segment is not intended as a claim of originality, but rather as a testament to
# the efficacy of the adopted approach.

class Interface(abc.ABC): pass


def interface(cls):
    attrs = {n: classmethod(abc.abstractmethod(f)) for n, f in inspect.getmembers(cls, predicate=inspect.isfunction)}
    return type(cls.__name__, (Interface, cls), attrs)


@interface
class Maya:
    def get_main_window(cls): pass
    def decode_utf8_string(cls, byte_string): pass
    def decode_fbxasc_string(cls, fbxasc_string): pass

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

@interface
class Packages:
    def reload(cls, packages): pass
    def upload(cls, packages): pass