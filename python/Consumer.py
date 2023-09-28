# currently redundant used if python consumer is required
from kafka import KafkaConsumer
from avro.datafile import DataFileReader
from avro.io import DatumReader
import io
import avro.schema

# Define the Avro schema
avro_schemaa = open("message.avsc", "rb").read()
avro_schema = avro.schema.parse(avro_schemaa.decode("utf-8"))

# Kafka Consumer Configuration
consumer = KafkaConsumer(
    'messages',  # Topic name
    bootstrap_servers='localhost:9092',
)

# Iterate over Kafka messages and deserialize Avro data
for message in consumer:
    avro_data = io.BytesIO(message.value)
    avro_reader = DataFileReader(avro_data, DatumReader(avro_schema))

    for record in avro_reader:
        print(record)  # This will print each Avro record

    avro_reader.close()
