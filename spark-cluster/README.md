# Running Spark Cluster on Docker

## 🌟 Make Docker Images
- **Download Docker Files**
   - cluster-base.Dockerfile
   - spark-base.Dockerfile
   - spark-masker.Dockerfile
   - spark-worker.Dockerfile
   - jupyterlab.Dockerfile
   - docker-compose.yml

- **Make Images**
```shell
# -- Building the Images

$ docker build \
  -f cluster-base.Dockerfile \
  -t cluster-base .

$ docker build \
  --build-arg spark_version="3.3.2" \
  --build-arg hadoop_version="2" \
  -f spark-base.Dockerfile \
  -t spark-base .

$ docker build \
  -f spark-master.Dockerfile \
  -t spark-master .

$ docker build \
  -f spark-worker.Dockerfile \
  -t spark-worker .

$ docker build \
  --build-arg spark_version="3.3.2" \
  --build-arg jupyterlab_version="2.1.5" \
  -f jupyterlab.Dockerfile \
  -t jupyterlab .
```

## 🌟 Compose up
```shell
$ docker-compose up -d
```

## 🌟 Compose down
```shell
$ docker-compose down
```

## :computer: Web UI
- **JupyterLab** at *localhost:8888*
- **Spark master** at *localhost:8080*
- **Spark worker I** at *localhost:8081*
- **Spark worker II** at *localhost:8082*

## 📝 spark-submit
```
$docker exec -it spark-master /usr/bin/spark-3.3.2-bin-hadoop2/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,org.apache.commons:commons-pool2:2.11.1,org.apache.kafka:kafka-clients:2.5.0,org.apache.spark:spark-streaming-kafka-0-10_2.12:3.3.2 spark-streaming.py
```

---

# Running by Makefile
## Compose up
```shell
$ make spark-cluster
```

## Compose down
```shell
$ make spark-cluster-clean
```
