spark-cluster:
	docker compose -f docker-compose.yaml up

spark-cluster-clean:
	docker compose down -v

spark-submit:
	docker exec -it spark-master /usr/bin/spark-3.3.2-bin-hadoop2/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,org.apache.commons:commons-pool2:2.11.1,org.apache.kafka:kafka-clients:2.5.0,org.apache.spark:spark-streaming-kafka-0-10_2.12:3.3.2 spark-streaming.py



# images build at once
dependency:
	docker build -f cluster-base.Dockerfile -t cluster-base .
	docker build --build-arg spark_version="3.3.2" --build-arg hadoop_version="2" -f spark-base.Dockerfile -t spark-base .
	docker build -f spark-master.Dockerfile -t spark-master .
	docker build -f spark-worker.Dockerfile -t spark-worker .
	docker build --build-arg spark_version="3.3.2" --build-arg jupyterlab_version="2.1.5" -f jupyterlab.Dockerfile -t jupyterlab .

# build each images
cluster-base:
	docker build -f cluster-base.Dockerfile -t cluster-base .

spark-base:
	docker build \
  	--build-arg spark_version="3.3.2" \
  	--build-arg hadoop_version="2" \
  	-f spark-base.Dockerfile \
  	-t spark-base .

spark-master:
	docker build \
  	-f spark-master.Dockerfile \
  	-t spark-master .

spark-worker:
	docker build \
	-f spark-worker.Dockerfile \
  	-t spark-worker .

jupyterlab:
	docker build \
	--build-arg spark_version="3.3.2" \
	--build-arg jupyterlab_version="2.1.5" \
	-f jupyterlab.Dockerfile \
	-t jupyterlab .