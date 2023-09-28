import express from "express";
import { queueMessage } from "./Producer.js";

const app = express();
const port = process.env.PORT || 8080;

app.use(express.json());

app.post('/send-message', (req, res) => {
  let message = req.body;
  message.object_type = "MSG";
  console.log(message);
  queueMessage(message);


  return res.send("sent message successfully!");
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
