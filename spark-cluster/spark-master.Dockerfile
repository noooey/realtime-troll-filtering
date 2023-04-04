FROM spark-base

# -- Runtime

ARG spark_master_web_ui=8080

COPY spark-streaming.py /usr/bin/spark-3.3.2-bin-hadoop2/

EXPOSE ${spark_master_web_ui} ${SPARK_MASTER_PORT}
CMD bin/spark-class org.apache.spark.deploy.master.Master >> logs/spark-master.out
