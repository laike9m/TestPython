from fastcore import typedispatch
from types import FunctionType

class Negator:

    @singledispatchmethod
    def __call__(self, function_or_disabled):
        pass


    @__call__.register
    def _(self, disabled: bool):
        def dec(f):

            def wrapper(*args):
                return f(*args)

            return wrapper

        return dec

    @__call__.register
    def _(self, function: FunctionType):
        print(function)
        return self.__call__(disabled=True)(function)


n = Negator()

@n
def f(x):
    return x


print(f(1))
