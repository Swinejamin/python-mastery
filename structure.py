import sys
import inspect


class Structure:
    _fields = ()

    @classmethod
    def create_init(cls):
        args = ','.join(cls._fields)
        code = 'def __init__(self, {0}):\n'.format(args)
        statements = ['    self.{0} = {0}'.format(name) for name in cls._fields]
        code += '\n'.join(statements)
        locs = {}
        exec(code, locs)
        cls.__init__ = locs['__init__']

    def __eq__(self, other):
        return isinstance(other, self.__class__) and (
            all([getattr(self, field) == getattr(other, field) for field in self._fields])
        )

    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError("Expected %d arguments" % len(self._fields))
        for name, arg in zip(self._fields, args):
            setattr(self, name, arg)

    def __repr__(self):
        return "%s(%s)" % (
            type(self).__name__,
            ", ".join(repr(getattr(self, name)) for name in self._fields),
        )

    def __setattr__(self, name, value):
        if name.startswith("_") or name in self._fields:
            super().__setattr__(name, value)
        else:
            raise AttributeError("No attribute %s" % name)
