console.log("producer started<:>");

import Kafka from 'node-rdkafka';
import eventType from "../eventType.js";

const stream = Kafka.Producer.createWriteStream ({
    'metadata.broker.list': 'kafka:9092'
}, {}, { topic: 'messages' });

export function queueMessage (event) {
    // const event = { object_type: "MSG", sender_id: "444", body: "body"};
    const success = stream.write(eventType.toBuffer(event));
    console.log(success);
}

// setInterval(() => {
//     queueMessage();
// }, 3000);

