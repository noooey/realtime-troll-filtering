from json import loads
from kafka import KafkaConsumer

# Create a Consumer Instance
consumer = KafkaConsumer(
            'youtube_comments',
            bootstrap_servers="broker:29092",
            auto_offset_reset="earliest",
            group_id="comments-consumer-group",
            value_deserializer=lambda x: loads(x),
            )

# Consume messages
for msg in consumer:
    print(msg)