# 通过把函数调用处的 bytecode 还原成 ast 来 track parameter

f = lambda x: x


def g(a, b, c, d):
    return a + b + c + d


a = 0

# fmt: off
g(a,
  (1 if True else 0),
  f(2),
  3)
# fmt: on

print("Program ends")
