import requests

import msgpack

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 1989  # The port used by the server

data = {
    "foo": [1, 42, 3.141, 1337, "help"],
    "bar": "bla",
    "baz": {"foo": "bar", "key": "value", "the answer": 42},
}


requests.post(
    f"http://{HOST}:{PORT}/frame",
    data=msgpack.packb(data),
    headers={"Content-Type": "application/octet-stream"},
)
