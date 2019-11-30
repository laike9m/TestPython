class ID:
    def __init__(self, tup):
        self._key = tup

    def __eq__(self, other):
        self._key == other._key

    def __hash__(self):
        return hash(self._key)


id1 = ID((0, 0))
id2 = ID((0, 0))

assert hash(id1) == hash(id2)  # pass
assert id1 == id2  # pass

a = {id1}
b = {id2}

assert a == b
