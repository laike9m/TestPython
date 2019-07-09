import pysnooper

@pysnooper.snoop(depth=2)
def main():

    def f(x, y, z):
      pass

    x = {
      1: 1,  # line event
      2: 2   # line event
    }
    a= 1
    f(a,  # line event
      2,    # line event
      f(1,
        2,
        3))    # line event


main()
