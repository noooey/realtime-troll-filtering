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

docker build \
  -f cluster-base.Dockerfile \
  -t cluster-base .

docker build \
  --build-arg spark_version="3.3.2" \
  --build-arg hadoop_version="2" \
  -f spark-base.Dockerfile \
  -t spark-base .

docker build \
  -f spark-master.Dockerfile \
  -t spark-master .

docker build \
  -f spark-worker.Dockerfile \
  -t spark-worker .

docker build \
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
