"""A doc string

foo
"""
import sys
import ast
import astor
import inspect

frame = sys._getframe()
print(frame.f_code.co_lnotab)
print(frame.f_code.co_firstlineno)


def f():
    x = 1
    frame = sys._getframe()
    print(frame.f_code.co_lnotab)
    print(frame.f_code.co_firstlineno)


f()
