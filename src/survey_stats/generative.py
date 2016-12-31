from functools import wraps

class GenerativeBase(object):
    def _generate(self):
        s = self.__class__.__new__(self.__class__)
        s.__dict__ = self.__dict__.copy()
        return s

def _generative(func):
    @wraps(func)
    def decorator(self, *args, **kwargs):
        new_self = self._generate()
        func(new_self, *args, **kwargs)
        return new_self
    return decorator
