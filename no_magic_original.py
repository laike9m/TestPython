from functools import lru_cache
from collections import namedtuple
from astpretty import pprint
import math
import bytecode as b
import uncompyle6 as unc
import sys
import opcode as _opcode
import ast
import io

MARK = "__MARK__"


Args = namedtuple('Args', ['args', 'kwargs'])

def _compute_offset(instr):
    opcode = instr._opcode
    arg = instr.arg
    if opcode < _opcode.HAVE_ARGUMENT:
            arg = 0
    elif not isinstance(arg, int) or opcode in _opcode.hasconst:
        arg = 0
    if arg is 0:
        return 2
    return math.ceil(math.log(arg + 1 , 256)) * 2

def compute_offset(instrs, i):
    assert isinstance(instrs, b.ConcreteBytecode)
    now = 0
    for index, instr in enumerate(instrs):
        now += _compute_offset(instr)
        if i <= now:
            break
    return index

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

@lru_cache()
def get_cache_code(code):

    bc = b.Bytecode.from_code(code)
    # arg of loading freevar/cellvar represented via integers
    concrete_bc = bc.to_concrete_bytecode()
    return bc, concrete_bc

@lru_cache()
def get_cache_callsite_ast(code, i):
    bc, cbc = get_cache_code(code)
    index = compute_offset(cbc, i)
    bc.insert(index + 1 + 1,  b.Instr('LOAD_ATTR', MARK))
    string_io = io.StringIO()
    unc.deparse_code2str(bc.to_code(), out=string_io)
    return ast.parse(string_io.getvalue())

class TheMonitor:
    __slots__ = ('f', )
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
        return self.f(callsite_arginfo , *args, **kwargs)


@TheMonitor
def f(formal_args, x, y):
    pprint(formal_args.args[0])
    pprint(formal_args.args[1])
    return x + y

def test(g):
    z = f(1, g)
    return z

test(1)