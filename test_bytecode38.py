from bytecode import Label, Instr, Bytecode

label_else = Label()
label_print = Label()
bytecode = Bytecode(
    [
        Instr("LOAD_NAME", "print"),
        Instr("LOAD_NAME", "test"),
        Instr("POP_JUMP_IF_FALSE", label_else),
        Instr("LOAD_CONST", "yes"),
        Instr("JUMP_FORWARD", label_print),
        label_else,
        Instr("LOAD_CONST", "no"),
        label_print,
        Instr("CALL_FUNCTION", 1),
        Instr("LOAD_CONST", None),
        Instr("RETURN_VALUE"),
    ]
)
code = bytecode.to_code()

test = 0
exec(code)

test = 1
exec(code)
