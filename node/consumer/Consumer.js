console.log("consumer started<:>");

import Kafka from "node-rdkafka";
import eventType from "../eventType.js";

import { saveMessageToDB } from "../save_message_to_db.js";

let order_num = 1;

const consumer = Kafka.KafkaConsumer({
    "group.id": "kafka",
    "metadata.broker.list": "kafka:9092"
}, {});

consumer.connect();

consumer.on("ready", () => {
    console.log("consumer is ready");
    consumer.subscribe(["messages"]);
    consumer.consume();
}).on("data", (data) => {
    let message = eventType.fromBuffer(data.value);
    let message_json = JSON.parse(message);
    delete message_json.object_type;
    message_json.order_num = order_num++;
    saveMessageToDB(message_json);
    console.log(`received message: ${JSON.stringify(message_json, null, 1)}`);
});
