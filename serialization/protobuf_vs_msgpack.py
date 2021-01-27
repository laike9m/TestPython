"""
Compares the serialization performance of protobuf vs msgpack.
"""


from datetime import datetime

import msgpack
from data_pb2 import Data


class PyData:
    def __init__(self):
        self.id = "1234567"
        self.lineno = 10
        self.index = 10000


data_lst = [PyData() for _ in range(1000000)]

start = datetime.now()

for pydata in data_lst:
    Data(id=pydata.id, lineno=pydata.lineno, index=pydata.index).SerializeToString()

end = datetime.now()
print(end - start)

start = datetime.now()
for pydata in data_lst:
    msgpack.packb({"id": pydata.id, "lineno": pydata.lineno, "index": pydata.index})
end = datetime.now()
print(end - start)
