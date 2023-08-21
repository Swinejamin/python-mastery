from logcall import logged, logformat


@logged
def add(x, y):
    'Adds two things'
    return x + y


@logged
def sub(x, y):
    return x - y


@logformat('{func.__code__.co_filename}:{func.__name__}')
def mul(x, y):
    return x * y


class Spam:
    @logged
    def instance_method(self):
        pass

    @logged
    @classmethod
    def class_method(cls):
        pass

    @logged
    @staticmethod
    def static_method():
        pass

    @logged
    @property
    def property_method(self):
        return 'property method return'


s = Spam()
print(s)
print(s.instance_method())
print(Spam.class_method())
print(Spam.static_method())
print(s.property_method)