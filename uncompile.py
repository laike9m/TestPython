import uncompyle6
import io
import sys, inspect


def uncompyle_test():
    frame = inspect.currentframe()
    try:
        co = frame.f_code
        string_io = io.StringIO()
        uncompyle6.deparse_code2str(co, out=string_io)
        print(string_io.getvalue())
    finally:
        del frame


uncompyle_test()
