import findspark
findspark.init()

from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, LongType
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, pandas_udf, split, from_json, expr
import pandas as pd
import nltk
from nltk.corpus import stopwords
from transformers import AutoTokenizer
import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import numpy as np
from tqdm import tqdm, tqdm_notebook

#kobert
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model

#regularization
import re
import emoji
from soynlp.normalizer import repeat_normalize

import json
#BERT 모델, Vocabulary 불러오기
bertmodel, vocab = get_pytorch_kobert_model()

max_len = 150
batch_size = 32

class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len,
                 pad, pair):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)
        length = len(dataset)
        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))

    def __len__(self):
        return (len(self.labels))


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


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


def getAttr(token_ls):
    columns = ['token_ids', 'valid_length', 'segment_ids', 'label']
    for i in range(3):
        token_ls[i] = token_ls[i].tolist()
    dic = dict(zip(columns, token_ls))
    json_val = json.dumps(dic, cls=NpEncoder)
    return json_val


# Define the processing function
def process(comments):
    comments = clean(comments)

    comments_tok = pd.DataFrame([[comments, '0']], columns=['comments', 'label'])
    comments_tok.to_csv('comments.tsv', sep='\t', encoding='utf-8', index=False)
    comments_tok = nlp.data.TSVDataset('comments.tsv', field_indices=[0,1], num_discard_samples=1)

    tokenizer = get_tokenizer()
    tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)
    # 토큰화
    data_comments = BERTDataset(comments_tok, 0, 1, tok, max_len, True, False)

    return getAttr(list(data_comments[0]))

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
process_udf = udf(lambda z:process(z), StringType())
df_processed = df \
    .select(from_json(col("value").cast("string"), SCHEMA).alias("value")) \
    .selectExpr('value.id', 'value.datetime', 'value.user', 'value.content') \
    .withColumn('content_processed', process_udf(col('content'))) \
    .drop('content') \
    .withColumnRenamed('content_processed', 'content')

# Write processed data to console
df_processed.writeStream \
    .format("console") \
    .option("truncate", "false") \
    .outputMode("append") \
    .start() \
    .awaitTermination()
