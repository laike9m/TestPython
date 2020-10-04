from cheap_repr import cheap_repr

def foo():
    def bar():
        pass

    print(cheap_repr(bar))


foo()
