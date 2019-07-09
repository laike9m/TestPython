# 展示各种 bytecode, ast-level 信息，用来快速测试

import inspect
import dis
import sys
import astor
import ast
import bytecode
import uncompyle6

from bytecode import Instr

import io


def last_i(*args):
    frame = sys._getframe(1)
    # what is f_lasti
    print(dis.dis(frame.f_code))
    print("f_lasti is: ", frame.f_lasti)

    # attribute as a marker
    print(astor.dump_tree(ast.parse("f().__MARK__")))


def dis_mark():
    print(dis.dis("f(1, g, (y + 1), (1 if True else 2)).__MARK__"))


def nested_function_line_event():
    def f(x, y):
        pass

    def g(x):
        return x

    def printer_global(frame, event, arg):
        print("frame.lineno is: ", frame.f_lineno)
        print("\nthis is global")
        print(frame, event, arg)
        return printer_local

    def printer_local(frame, event, arg):
        print("frame.lineno is: ", frame.f_lineno)
        print(frame, event, arg)

    sys.settrace(printer_global)
    sys._getframe().f_trace = printer_local
    f(1, g(2))
    sys.settrace(None)


def bytecode_test():
    def f():
        # create a local scope
        return sys._getframe().f_code

    code = f()
    bc = bytecode.Bytecode.from_code(code)
    print(astor.dump_tree(bc))
    bc.pop()
    print(len(code.co_code))


def pdb_in_trace_func():
    def g(x):
        return x

    def tracer(frame, event, arg):
        breakpoint()
        print("\nthis is global")
        print(frame, event, arg)

    sys.settrace(tracer)
    g(2)


def bytecode_truncate():
    def f():
        a = 1
        b = 2
        return sys._getframe()

    def _compute_offset(instr):
        if sys.version_info >= (3, 6):
            return 2
        return (1, 3)[instr._opcode < _opcode.HAVE_ARGUMENT]

    frame = f()

    python_Bytecode = dis.Bytecode(frame.f_code)
    print(python_Bytecode.first_line)
    print(python_Bytecode.info())

    bc = bytecode.Bytecode.from_code(frame.f_code)

    print("original bytecode: ")
    for b in bc:
        print(b)

    start = 2
    end = 4
    i = 0
    start_bc = end_bc = None
    for j, instr in enumerate(bc):
        if start_bc is None and i >= start:
            start_bc = j
        if end_bc is None and i >= end:
            end_bc = j
        if type(instr) != bytecode.Instr:
            continue
        i += _compute_offset(instr)

    del bc[end_bc:]
    del bc[:start_bc]

    print("\nmodified bytecode: ")
    for b in bc:
        print(b)


def uncompile_load_name():
    bc = bytecode.Bytecode(
        [
            Instr("LOAD_NAME", "print"),
            Instr("LOAD_CONST", "Hello World!"),
            Instr("CALL_FUNCTION", 1),
            Instr("POP_TOP"),
            Instr("LOAD_CONST", None),
            Instr("RETURN_VALUE"),
        ]
    )
    # uncompyle6.deparse_code2str(bc.to_code(), out=sys.stdout)
    print(inspect.getsource(sys._getframe()))
    print(sys._getframe().f_code.co_lnotab)


def call_stdlib():
    import sys
    import os

    def tracer(frame, event, arg):
        print(frame, event, arg)
        return tracer

    sys.settrace(tracer)
    os.environ.get("CLINT_FORCE_COLOR")


def lnotab_and_comments():
    def f():
        """sdsds
        """
        frame = sys._getframe()
        # foo
        # bar
        return frame

    print(f().f_code.co_lnotab)


def main():
    lnotab_and_comments()


if __name__ == "__main__":
    main()
