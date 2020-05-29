import sys
import gc
from pprint import pprint
import executing


def f():
    return sys._getframe()


class A:
    def do(self):
        executing_obj = executing.Source.executing(sys._getframe())
        node = list(executing_obj.statements)[0]
        print(node)
        while hasattr(node, "parent") and node.parent:
            print(node.parent)
            node = node.parent


a = A()
a.do()
