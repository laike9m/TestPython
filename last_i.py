import sys


def global_tracer(frame, event_type, arg):
    print("last_i: ", frame.f_back.f_lasti)  # Win: 38, Mac: 40


sys.settrace(global_tracer)


def f():
    pass


f()
