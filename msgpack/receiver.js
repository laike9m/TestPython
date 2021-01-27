import pkg from "@msgpack/msgpack";
import dgram from "dgram";

const { decode } = pkg;

let cl = console.log;

const PORT = 3000;

const server = dgram.createSocket("udp4");

server.on("error", err => {
  console.log(`server error:\n${err.stack}`);
  server.close();
});

server.on("message", (msg, rinfo) => {
  console.log(`server got: msg from ${rinfo.address}:${rinfo.port}`);
  const object = decode(msg.buffer);
  console.log(object);
  console.log(`baz.foo is ${object.baz.foo}`);
});

server.on("listening", () => {
  const address = server.address();
  console.log(`server listening ${address.address}:${address.port}`);
});

server.bind(PORT);
// Prints: server listening 0.0.0.0:41234
