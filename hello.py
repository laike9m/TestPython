from cyberbrain import Tracer

tracer = Tracer()
tracer.init()

a = 1
b = a

tracer.register()

c = 1
# print(tracer.events)