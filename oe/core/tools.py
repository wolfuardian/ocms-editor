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



# fmt: on
