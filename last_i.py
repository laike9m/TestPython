import gc
import inspect
import sys


def global_tracer(frame, event_type, arg):
    if event_type == "call" and frame.f_code == gen.__code__:
        print(gc.get_referrers(frame))
        print(frame.f_lasti, event_type)
        frame.f_trace_opcodes = True
        return local_tracer


def local_tracer(frame, event_type, arg):
    print(frame.f_lasti, event_type)


sys.settrace(global_tracer)


def gen():
    for i in range(3):
        yield i


g = gen()
g2 = gen()

print(inspect.getgeneratorstate(g))

next(g)
print(inspect.getgeneratorstate(g))
next(g)
print(inspect.getgeneratorstate(g))
next(g)
print(inspect.getgeneratorstate(g))
try:
    next(g)
except StopIteration:
    pass
print(inspect.getgeneratorstate(g))
print(type(inspect.getgeneratorstate(g)))
