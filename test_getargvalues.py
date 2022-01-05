import inspect


def f(foo, bar, baz=1, *args, **kwargs):
    frame = inspect.currentframe()
    print(inspect.getargvalues(frame))


f(1, 2, 3, 5, 6, kkl=3)

f(1, 2, baz=4, fff=5)


def g():
    frame = inspect.currentframe()
    print(inspect.getargvalues(frame))


g()
