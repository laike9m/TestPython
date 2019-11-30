from birdseye import eye, server


class A:
    def __init__(self, x, y):
        self.x = x
        self.y = y


@eye
def f():
    a = A(1, 2)
    b = A(3, a)


f()

server.app.run(host="0.0.0.0", port=7777)
