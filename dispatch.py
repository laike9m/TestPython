from functools import singledispatchmethod
from types import FunctionType

class Negator:

    @singledispatchmethod
    def __call__(self, arg):
        pass

    def dec(self, f):
        def wrapper(*args):
            return f(*args)

        return wrapper

    @__call__.register
    def _(self, arg: bool):
        return self.dec

    @__call__.register
    def _(self, arg: FunctionType):
        return self.dec(lambda x: 1)


n = Negator()


@n
def f(x):
    return x


print(f(1))

@n(True)
def g(x):
    return x


print(g(1))
