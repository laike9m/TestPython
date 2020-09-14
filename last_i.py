import sys


def global_tracer(frame, event_type, arg):
    if event_type == "call" and frame.f_code == f.__code__:
        print(frame.f_lasti, event_type)
        frame.f_trace_opcodes = True
        return local_tracer


def local_tracer(frame, event_type, arg):
    print(frame.f_lasti, event_type)


sys.settrace(global_tracer)


def f(x):
    a = 1
    b = 2


f(1)
