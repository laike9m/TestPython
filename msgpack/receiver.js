import pkg from "@msgpack/msgpack";
import express from "express";
import bodyParser from "body-parser";

const { decode } = pkg;

let cl = console.log;

const app = express();
app.use(bodyParser.raw());

app.post("/frame", function(req, res) {
  const object = decode(req.body);
  console.log(object);
  console.log(`baz.foo is ${object.baz.foo}`);
  res.send("POST request to homepage");
});

app.listen(3000, () => console.log("Example app listening on port 3000!"));
