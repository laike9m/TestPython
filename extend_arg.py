# Tests how EXTENDED_ARG works

import bytecode
import dis
import sys
from bytecode import ConcreteInstr, ConcreteBytecode

CONST_ARG = 0x1234567  # The real argument we want to set.
cbc = bytecode.ConcreteBytecode()
cbc.consts = [None] * (CONST_ARG + 1)  # Make sure co_consts is big enough.
cbc.consts[CONST_ARG] = "foo"  # Sets co_consts manually.

if sys.version_info >= (3, 6):
    cbc.extend(
        [
            ConcreteInstr("EXTENDED_ARG", 0x1),
            ConcreteInstr("EXTENDED_ARG", 0x23),
            ConcreteInstr("EXTENDED_ARG", 0x45),
            ConcreteInstr("LOAD_CONST", 0x67),
            ConcreteInstr("RETURN_VALUE"),
        ]
    )
else:
    cbc.extend(
        [
            ConcreteInstr("EXTENDED_ARG", 0x123),
            ConcreteInstr("LOAD_CONST", 0x4567),
            ConcreteInstr("RETURN_VALUE"),
        ]
    )

code = cbc.to_code()
dis.dis(code)

ext0, ext1, ext2, load_const = list(dis.get_instructions(code))[:4]
print("ext0 arg is: ", ext0.arg)
print("ext1 arg is: ", ext1.arg)
print("ext2 arg is: ", ext2.arg)
print("ext2 arg is: ", load_const.arg, ", value is:", load_const.argval)

for raw_byte in code.co_code:
    print("raw code is: ", raw_byte)
