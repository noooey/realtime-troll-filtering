import pytchat # crawling realtime comments
import pafy # video information
import json
from kafka import KafkaProducer
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Get Youtube API key and Video Id
YOUTUBE_API_KEY = config['youtube']['api_key']
VIDEO_ID = config['youtube']['video_id']

# Set API key on Pafy
pafy.set_api_key(YOUTUBE_API_KEY)

# Create the Pychate Instance
chat = pytchat.create(video_id=VIDEO_ID)

# Create a Producer Instance
producer = KafkaProducer(
            # bootstrap_servers='localhost:9092',
            bootstrap_servers='broker:29092',
            key_serializer = None,
            value_serializer = lambda v: json.dumps(v).encode("utf-8")
            )

# Scrap Chat data with PytChat
while chat.is_alive():
    try:
        for c in chat.get().sync_items():
            data = {
                "id": c.id,
                "datetime": c.datetime,
                "author": c.author.name,
                "message": c.message
            }
            print(data)
            producer.send('youtube_comments', data)
    except KeyboardInterrupt:
        chat.terminate()
        break