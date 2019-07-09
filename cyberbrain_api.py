import sys
import inspect
import sysconfig
from functools import lru_cache

paths = list(sysconfig.get_paths().values())
print(paths)


@lru_cache()
def should_exclude(filename):
    if "importlib" in filename:
        return True
    for path in paths:
        if filename.startswith(path):
            return True
    return False


def printer_global(frame, event, arg):
    print(frame.f_code.co_filename)
    if should_exclude(frame.f_code.co_filename):
        return
    print(frame, event, arg)
    return printer_local


def printer_local(frame, event, arg):
    if should_exclude(frame.f_code.co_filename):
        return
    print(frame, event, arg)


sys.settrace(printer_global)
sys._getframe().f_trace = printer_local
