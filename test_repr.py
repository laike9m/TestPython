from cheap_repr import cheap_repr

def this_is_my_function():
    class A:
        pass

    a = A()

    print(cheap_repr(a))
    from utils import return_GetFrame

    frame = return_GetFrame(rpc)


this_is_my_function()
