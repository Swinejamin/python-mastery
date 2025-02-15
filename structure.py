from validate import Validator, validated
from collections import ChainMap


class StructureMeta(type):
    @classmethod
    def __prepare__(meta, clsname, bases):
        return ChainMap({}, Validator.validators)

    @staticmethod
    def __new__(meta, name, bases, methods):
        methods = methods.maps[0]
        return super().__new__(meta, name, bases, methods)


class Structure(metaclass=StructureMeta):
    _fields = ()
    _types = ()

    def __iter__(self):
        for name in self._fields:
            yield getattr(self, name)

    def __eq__(self, other):
        return isinstance(other, type(self)) and tuple(self) == tuple(other)

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

    @classmethod
    def __init_subclass__(cls):
        validate_attributes(cls)

    @classmethod
    def create_init(cls):
        """
        Create an __init__ method from _fields
        """
        args = ",".join(cls._fields)
        code = "def __init__(self, {0}):\n".format(args)
        statements = ["    self.{0} = {0}".format(name) for name in cls._fields]
        code += "\n".join(statements)
        locs = {}
        exec(code, locs)
        cls.__init__ = locs["__init__"]

    @classmethod
    def from_row(cls, row):
        rowdata = [func(val) for func, val in zip(cls._types, row)]
        return cls(*rowdata)


def validate_attributes(cls):
    """
    Class decorator that scans a class definition for Validators
    and builds a _fields variable that captures their definition order.
    """
    validators = []
    for name, val in vars(cls).items():
        if isinstance(val, Validator):
            validators.append(val)
        # Apply validated decorator to any callable with annotations
        elif callable(val) and val.__annotations__:
            setattr(cls, name, validated(val))

    # Collect all the field names
    cls._fields = tuple([v.name for v in validators])

    # Collect type conversions. The lambda x:x is an identity
    # function that's used in case no expected_type is found.
    cls._types = tuple([getattr(v, "expected_type", lambda x: x) for v in validators])

    # Create the __init__ method
    if cls._fields:
        cls.create_init()

    return cls


def typed_structure(clsname, **validators):
    cls = type(clsname, (Structure,), validators)
    return cls
