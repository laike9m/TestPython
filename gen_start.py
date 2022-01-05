import dis


def generator_function(count):
    while count > 0:
        a = 1
        # yield count
        # count -= 1


print(list(generator_function.__code__.co_lines()))

print(list(dis.findlinestarts(generator_function.__code__)))
