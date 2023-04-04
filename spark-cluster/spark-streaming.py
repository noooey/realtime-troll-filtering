import findspark
findspark.init()

# from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, LongType
# from pyspark.sql import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, pandas_udf, split, from_json, expr

KAFKA_BOOTSTRAP_SERVERS = "broker-1:29092, broker-2:29093, broker-3:29094"
KAFKA_TOPIC = "youtube_comments"

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

# df.awaitTermination()

# Write stream - console
# df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
#     .writeStream \
#     .format("console") \
#     .outputMode("append") \
#     .start() \
#     .awaitTermination()
df.select(from_json(col("value").cast("string"), SCHEMA).alias("value")) \
    .selectExpr('value.id', 'value.datetime', 'value.user', 'value.content') \
    .writeStream \
    .format("console") \
    .outputMode("append") \
    .start() \
    .awaitTermination()