from inspect import signature
from functools import wraps


class Validator:
    # Collect all derived classes into a dict
    validators = {}

    def __init__(self, name=None):
        self.name = name

    def __set_name__(self, cls, name):
        self.name = name

    @classmethod
    def check(cls, value):
        return value

    @classmethod
    def __init_subclass__(cls):
        cls.validators[cls.__name__] = cls

    def __set__(self, instance, value):
        instance.__dict__[self.name] = self.check(value)


class Typed(Validator):
    expected_type = object

    @classmethod
    def check(cls, value):
        if not isinstance(value, cls.expected_type):
            raise TypeError(f"Expected {cls.expected_type}")
        return super().check(value)


class Integer(Typed):
    expected_type = int


class Float(Typed):
    expected_type = float


class String(Typed):
    expected_type = str


class Positive(Validator):
    @classmethod
    def check(cls, value):
        if value < 0:
            raise ValueError("Expected >= 0")
        return super().check(value)


class NonEmpty(Validator):
    @classmethod
    def check(cls, value):
        if len(value) == 0:
            raise ValueError("Must be non-empty")
        return super().check(value)


class PositiveInteger(Integer, Positive):
    pass


class PositiveFloat(Float, Positive):
    pass


class NonEmptyString(String, NonEmpty):
    pass


def validated(func):
    sig = signature(func)

    # Gather the function annotations
    annotations = dict(func.__annotations__)

    # Get the return annotation (if any)
    retcheck = annotations.pop("return", None)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, *kwargs)
        errors = []

        # Enforce argument checks
        for name, validator in annotations.items():
            try:
                validator.check(bound.arguments[name])
            except Exception as e:
                errors.append(f"    {name}: {e}")

        if errors:
            raise TypeError("Bad Arguments\n" + "\n".join(errors))

        for name, val in annotations.items():
            val.check(bound.arguments[name])

        result = func(*args, **kwargs)

        # Enforce return check (if any)
        if retcheck:
            try:
                retcheck.check(result)
            except Exception as e:
                raise TypeError(f"Bad return: {e}") from None
        return result

    return wrapper


def enforce(**annotations):
    retcheck = annotations.pop("return_", None)

    def decorate(func):
        sig = signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            errors = []

            # Enforce argument checks
            for name, validator in annotations.items():
                try:
                    validator.check(bound.arguments[name])
                except Exception as e:
                    errors.append(f"    {name}: {e}")

            if errors:
                raise TypeError("Bad Arguments\n" + "\n".join(errors))

            result = func(*args, **kwargs)

            if retcheck:
                try:
                    retcheck.check(result)
                except Exception as e:
                    raise TypeError(f"Bad return: {e}") from None
            return result

        return wrapper

    return decorate


@enforce(x=Integer, y=Integer, return_=Integer)
def add(x, y):
    return x + y


# print(add(2,3.0))
# print(add('two',3.0))
