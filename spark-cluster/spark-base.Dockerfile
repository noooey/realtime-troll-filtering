FROM cluster-base

# -- Layer: Apache Spark

ARG spark_version=3.3.2
ARG hadoop_version=2

RUN apt-get update -y && \
    pip3 install --upgrade pip setuptools wheel && \
    pip3 install pandas && \
    pip3 install findspark && \
    apt-get install git -y && \
    pip3 install git+https://git@github.com/SKTBrain/KoBERT.git@master && \
    pip3 install mxnet-mkl==1.6.0 numpy==1.23.1 && \
    pip3 install gluonnlp pandas tqdm && \
    pip3 install sentencepiece && \
    pip3 install transformers && \
    pip3 install torch && \
    pip3 install boto3 && \
    pip3 install nltk && \
    pip3 install emoji && \
    pip3 install soynlp && \
    pip3 install requests && \
    apt-get install -y curl && \
    curl https://archive.apache.org/dist/spark/spark-${spark_version}/spark-${spark_version}-bin-hadoop${hadoop_version}.tgz -o spark.tgz && \
    tar -xf spark.tgz && \
    mv spark-${spark_version}-bin-hadoop${hadoop_version} /usr/bin/ && \
    mkdir /usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}/logs && \
    rm spark.tgz

ENV SPARK_HOME /usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}
ENV SPARK_MASTER_HOST spark-master
ENV SPARK_MASTER_PORT 7077
ENV PYSPARK_PYTHON python3

# -- Runtime

WORKDIR ${SPARK_HOME}
