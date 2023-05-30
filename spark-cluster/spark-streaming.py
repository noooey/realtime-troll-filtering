import findspark
findspark.init()

from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, LongType
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, pandas_udf, split, from_json, expr

#regularization
import re
import emoji
import argparse
from soynlp.normalizer import repeat_normalize

import requests
import json

# Parse the command-line arguments
parser = argparse.ArgumentParser(description='Real-time YouTube comments crawler')
parser.add_argument('--kafka_topics', type=str, help='Kafka Topics')

args = parser.parse_args()

KAFKA_BOOTSTRAP_SERVERS = "broker-1:29092, broker-2:29093, broker-3:29094"
KAFKA_TOPIC = args.kafka_topics  # kafka cluster 내의 모든 topic에서 메세지 가져오도록 설정

# Create Schema
SCHEMA = StructType([
    StructField("id", StringType(), True),           # COMMENT ID
    StructField("datetime", TimestampType(), True),  # Date and hour
    StructField("user", StringType(), True),         # USER NAME
    StructField("content", StringType(), True),      # CONTENT
])

# Create a Spark Session
spark = SparkSession \
    .builder \
    .appName("kafka-streaming") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

spark.sparkContext.setLogLevel('WARN')


# Define the FastAPI endpoint URL
fastapi_url = "http://172.23.0.15:8000/predict"
headers = {"Content-Type": "application/json"}

# Define the function to send a request to the FastAPI endpoint
def send_request(data):
    response = requests.post(fastapi_url, headers=headers, data=data)
    return response


# 정규화
emojis = ''.join(emoji.EMOJI_DATA.keys())
pattern = re.compile(f'[^ .,?!/@$%~％·∼()\x00-\x7Fㄱ-힣{emojis}]+')
url_pattern = re.compile(
    r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')

def clean(x):
    x = pattern.sub(' ', x)
    x = url_pattern.sub('', x)
    x = x.strip()
    x = repeat_normalize(x, num_repeats=2)
    return x

# Define the processing function
def process(ids, comments):
    comments = clean(comments)
    json_val = {"id":ids, "sentence":comments}
    json_val = json.dumps(json_val)
    send_request(json_val)
    return comments


# Using Spark Structed Streaming
# Read messages from Kafka Topic and Create Dataframe
df = spark \
    .readStream\
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("failOnDataLoss","False") \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()


# Apply processing function to the content column
# Start the Spark Streaming job and iterate over the output rows
process_udf = udf(lambda x,y:process(x,y), StringType())
df_processed = df \
    .select(from_json(col("value").cast("string"), SCHEMA).alias("value")) \
    .selectExpr('value.id', 'value.datetime', 'value.user', 'value.content') \
    .withColumn('content_processed', process_udf(col('id'), col('content'))) \
    .drop('content') \
    .withColumnRenamed('content_processed', 'content')

df_processed.writeStream  \
    .format("console") \
    .option("truncate", "false") \
    .outputMode("append") \
    .start() \
    .awaitTermination()
