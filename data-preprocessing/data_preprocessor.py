from json import loads
from kafka import KafkaConsumer

# Create a Consumer Instance
consumer = KafkaConsumer(
            'youtube_comments',
            bootstrap_servers=["broker-1:29092", "broker-2:29093", "broker-3:29094"],
            auto_offset_reset="earliest",
            group_id="comments-consumer-group",
            value_deserializer=lambda x: loads(x),
            )

# Consume messages
for msg in consumer:
    print(msg)