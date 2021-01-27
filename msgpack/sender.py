import socket

import msgpack

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3000  # The port used by the server

data = {
    "foo": [1, 42, 3.141, 1337, "help"],
    "bar": "bla",
    "baz": {"foo": "bar", "key": "value", "the answer": 42},
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(msgpack.packb(data))
    s.close()
