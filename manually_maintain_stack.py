import dis
import sys


def g(x, y):
    # Code that analyzes outer frame to get passed in arguments.
    outer_frame = sys._getframe(1)
    instructions = list(dis.get_instructions(outer_frame.f_code))

    call_start_offset = None
    call_end_offset = None
    for index, instr in enumerate(instructions):
        if instr.starts_line and instr.starts_line > outer_frame.f_lineno:
            call_end_offset = index
            break
        # Assuming we already know the function name is 'g'.
        if instr.argval == 'g':
            call_start_offset = index

    # Manually record top of stack
    TOS = []
    arguments_from_outside = []
    for instr in instructions[call_start_offset:call_end_offset]:
        if instr.opname == 'LOAD_NAME':
            TOS.append((instr.argval, outer_frame.f_locals[instr.argval]))
        elif instr.opname == 'LOAD_CONST':
            TOS.append((instr.argval, None))
        elif instr.opname == 'CALL_FUNCTION':
            # Pops instr.arg elements from Top of stack, they are passed in arguments.
            arguments_from_outside.extend(TOS[-instr.arg:])


    print(arguments_from_outside)

a = 1
g(a,
  2)

print('Program ends')
