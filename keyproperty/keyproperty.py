"""
Convenience for:



class MyClass(collections.Mapping):
    @property
    def account(self):
        return self['account']


"""
import functools


class KPException(Exception):
    pass

class KPAttributeError(KPException, AttributeError):
    pass

class KPKeyError(KPException, KeyError):
    pass

def default_fget(self, key=None):
    return self[key]
def default_fset(self, value, key=None):
    self[key] = value
def default_fdel(self, key=None):
    del self[key]


def _get_descriptor(descriptor, default):
    """
    @type: descriptor:
    @type: descriptor:
    @rtype: collections.Callable or None
    """
    if callable(descriptor):
        return descriptor
    elif descriptor:  # True --> use default function
        return default
    else:  # False or None
        return None

class KeyProperty(object):
    def __init__(self, key, fget=True, fset=False, fdel=False):
        self._key = key   # key should not be changed

        self.fget = _get_descriptor(
            fget, functools.partial(default_fget, key=self.key))
        self.fset = _get_descriptor(
            fset, functools.partial(default_fset, key=self.key))
        self.fdel = _get_descriptor(
            fdel, functools.partial(default_fdel, key=self.key))

    @property
    def key(self):
        return self._key

    # Descriptors
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise KPAttributeError("Unreadable attribute.")
        try:
            return self.fget(obj)
        except KeyError:
            raise KPKeyError(self.key)

    def __set__(self, obj, value):
        if self.fset is None:
            raise KPAttributeError("Can not set attribute.")
        try:
            self.fset(obj, value)
        except KeyError:
            raise KPKeyError(self.key)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("Can not delete attribute.")
        try:
            self.fdel(obj)
        except KeyError:
            raise KPKeyError(self.key)


