import findspark
findspark.init()

from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.functions import col, pandas_udf, split

#sparkSession 생성
sc = SparkSession \
    .builder \
    .appName("kafka-streaming") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# spark structured streaming을 이용
# kafka에서 데이터를 읽어와 dataframe 생성
df = sc \
    .readStream\
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker-1:29092, broker-2:29093, broker-3:29094") \
    .option("failOnDataLoss","False") \
    .option("subscribe", "youtube_comments") \
    .option("startingOffsets", "earliest") \
    .load()

df.awaitTermination()
# 
# # Write stream - console
# query = df.selectExpr("CAST(value AS STRING)") \
# .writeStream \
# .format("console") \
# .option("truncate", "false") \
# .start()
# .awaitTermination()
