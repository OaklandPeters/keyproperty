import functools

class DictProperty(property):
    def __new__(cls, key):
        if not isinstance(key, basestring):
            raise TypeError("'key' must be a string.")

        def fget(self):
            return self[key]
        def fset(self, value):
            self[key] = value
        def fdel(self):
            del self[key]

        return property(fget, fset, fdel)




