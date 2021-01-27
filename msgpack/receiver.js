import * as net from "net";
import pkg from "@msgpack/msgpack";

const { decode } = pkg;

let cl = console.log;

class Data {
  constructor(obj) {
    Object.assign(this, obj);
  }
}

const PORT = 3000;
const IP = "127.0.0.1";
const BACKLOG = 10;

cl(`Listening on ${PORT}`);

net
  .createServer()
  .listen(PORT, IP, BACKLOG)
  .on("connection", socket =>
    socket.on("data", buffer => {
      const object = decode(buffer.buffer);
      console.log(object);
      console.log(`baz.foo is ${object.baz.foo}`);
      socket.end();
    })
  );
