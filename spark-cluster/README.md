# Running Spark Cluster on Docker

## 🌟 Make Docker Images
- **Download Docker Files**
   - cluster-base.DockerFile
   - spark-base.DockerFile
   - spark-masker.DockerFile
   - spark-worker.DockerFile
   - jupyterlab.DockerFile
   - docker-compose.yml

- **Make Images**
```shell
# -- Building the Images

$ docker build \
  -f cluster-base.DockerFile \
  -t cluster-base .

$ docker build \
  --build-arg spark_version="3.3.2" \
  --build-arg hadoop_version="2" \
  -f spark-base.DockerFile \
  -t spark-base .

$ docker build \
  -f spark-master.DockerFile \
  -t spark-master .

$ docker build \
  -f spark-worker.DockerFile \
  -t spark-worker .

$ docker build \
  --build-arg spark_version="3.3.2" \
  --build-arg jupyterlab_version="2.1.5" \
  -f jupyterlab.DockerFile \
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
