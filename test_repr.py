from cheap_repr import cheap_repr

def this_is_my_function():
    def bar():
        pass

    print(cheap_repr(bar))


this_is_my_function()
