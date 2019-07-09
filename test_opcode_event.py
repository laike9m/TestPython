#! /usr/bin/env python3
import dis
import sys


def main():
    dis.dis(add)
    sys.settrace(get_trace(False, get_callback(celebrate)))
    total = add(1, 2)
    print(f'total = {total}')
    sys.settrace(None)
    total = add(3, 4)
    print(f'total = {total}')
    print('Done')


def get_trace(trace_lines=True, opcode_callback=None):
    trace_opcodes = callable(opcode_callback)

    # noinspection PyUnusedLocal
    def trace(frame, event, arg):
        frame.f_trace_lines = trace_lines
        frame.f_trace_opcodes = trace_opcodes
        if trace_opcodes and event == 'opcode':
            opcode = frame.f_code.co_code[frame.f_lasti]
            opname = dis.opname[opcode]
            opcode_callback(frame, opcode, opname)
        return trace

    return trace


def get_callback(return_handler=None):
    handle_return = callable(return_handler)

    def echo_opcode(frame, opcode, opname):
        print(f'# {opname} ({opcode}) #')
        if handle_return and opcode == dis.opmap['RETURN_VALUE']:
            return_handler(frame)

    return echo_opcode


# noinspection PyUnusedLocal
def celebrate(frame):
    print('/-------------------\\')
    print('| We are returning! |')
    print('\\-------------------/')


def add(a, b):
    return a + b


if __name__ == '__main__':
    main()
