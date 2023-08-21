from functools import wraps, update_wrapper

WRAPPER_ASSIGNMENTS = ('__module__',
                       '__name__', '__qualname__', '__doc__',
                       '__annotations__')
WRAPPER_UPDATES = ('__dict__',)


class object_proxy(object):

    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__name__ = wrapped.__name__
        except AttributeError:
            pass

    @property
    def __class__(self):
        return self.wrapped.__class__

    def __getattr__(self, name):
        return getattr(self.wrapped, name)


def update_wrapper(wrapper, wrapped,
                   assigned=WRAPPER_ASSIGNMENTS,
                   updated=WRAPPER_UPDATES):
    wrapper.__wrapped__ = wrapped
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        getattr(wrapper, attr).update(
            getattr(wrapped, attr, {}))


class bound_function_wrapper(object_proxy):

    def __init__(self, wrapped):
        super(bound_function_wrapper, self).__init__(wrapped)

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)


class function_wrapper(object_proxy):

    def __init__(self, wrapped):
        super(function_wrapper, self).__init__(wrapped)

    def __get__(self, instance, owner):
        wrapped = self.wrapped.__get__(instance, owner)
        return bound_function_wrapper(wrapped)

    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)


def logformat(fmt):
    def logged(func):
        final_func= func
        if hasattr(func, '__func__'):
            final_func  = func.__func__
            print(func.__func__.__str__())

        name = func.fget.__name__ if type(func) == property else func.__name__
        # print('Adding logging to', name)

        @wraps(func)
        def wrapper(*args, **kwargs):
            print(fmt.format(func=func))
            return final_func(*args, **kwargs)

        return wrapper

    return logged


logged = logformat('Calling {func.__name__}')
