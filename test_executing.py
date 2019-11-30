import sys

import executing
import astpretty


def f():
    node = executing.Source.executing(sys._getframe(1)).node
    astpretty.pprint(node)


f()
