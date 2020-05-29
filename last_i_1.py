import sys


def global_tracer(frame, event_type, arg):
    print("last_i: ", frame.f_back.f_code.co_lnotab)


sys.settrace(global_tracer)

x = [1 for i in range(3)]