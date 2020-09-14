import sys


def global_tracer(frame, event_type, arg):
    print("last_i: ", frame.f_back.f_lasti)  # Win: 38, Mac: 40
    print(f"computed gotos enabled: {frame.f_back.f_lasti==40}")


sys.settrace(global_tracer)

x = [1 for i in range(3)]
