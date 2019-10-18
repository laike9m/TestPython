from functools import lru_cache
from collections import namedtuple
import math
import bytecode as b
import uncompyle6 as unc
import sys
import opcode as _opcode
import ast
import io
import astpretty
import dis

MARK = "__MARK__"


Args = namedtuple("Args", ["args", "kwargs"])


def _compute_offset(instr):
    if sys.version_info >= (3, 6):
        return 2
    return (1, 3)[instr._opcode < _opcode.HAVE_ARGUMENT]


def compute_offset(instrs: b.Bytecode, i):
    now = 0
    for index, instr in enumerate(instrs):
        # Only real instruction should increase offset
        if type(instr) != b.Instr:
            print("type is ", type(instr))
            continue
        now += _compute_offset(instr)
        if i <= now:
            break
    # We stop at instruction before CALL_XXX, by adding 2 we get instr after CALL_XXX.
    return index + 2


class GetArgInfo(ast.NodeVisitor):
    def __init__(self):
        self.activated = False
        self.result = None

    def visit_Attribute(self, node):
        if node.attr == MARK:
            self.activated = True
            self.visit(node.value)
            self.activated = False

    def visit_Call(self, node):
        self.visit(node.func)
        if self.activated:
            self.result = Args(node.args, node.keywords)
        for each in node.args:
            self.visit(each)
        for each in node.keywords:
            self.visit(each)


def get_cache_code(code):
    bc = b.Bytecode.from_code(code)
    # arg of loading freevar/cellvar represented via integers
    concrete_bc = bc.to_concrete_bytecode()
    return bc, concrete_bc


@lru_cache()
def get_cache_callsite_ast(code, i):
    bc, cbc = get_cache_code(code)

    print(dis.dis(code))
    print("\nfrom cbc:")
    for j, inst in enumerate(bc):
        print(j, inst)
    print("last i: ", i)

    index = compute_offset(bc, i)

    print("inserted at: ", index)

    i = 0
    for real_index, instr in enumerate(bc):
        # Again, we need to skip non-instruction object.
        if i == index:
            bc.insert(real_index, b.Instr("LOAD_ATTR", MARK))
            break
        if type(instr) != b.Instr:
            print("type is ", type(instr))
            continue
        i += 1

    print("after insertion")
    for j, inst in enumerate(bc):
        print(j, inst)

    string_io = io.StringIO()
    unc.deparse_code2str(bc.to_code(), out=string_io)
    # print(string_io.getvalue())
    return ast.parse(string_io.getvalue())


class TheMonitor:
    __slots__ = ("f",)

    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        f = sys._getframe(1)
        i = f.f_lasti
        callsite_ast = get_cache_callsite_ast(f.f_code, i)

        arginfo_visitor = GetArgInfo()
        arginfo_visitor.visit(callsite_ast)

        callsite_arginfo = arginfo_visitor.result
        assert callsite_arginfo
        for arg in callsite_arginfo.args:
            astpretty.pprint(arg)
        return self.f(*args, **kwargs)


@TheMonitor
def f(*args, **kwargs):
    x = [1 for i in range(3)]


def test():
    f(1, 2)


test()
