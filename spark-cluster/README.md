# Running Spark Cluster on Docker

## Download Dockerfiles
- cluster-base.Dockerfile
- spark-base.Dockerfile
- spark-masker.Dockerfile
- spark-worker.Dockerfile
- jupyterlab.Dockerfile
- docker-compose.yml

## Build Images
```shell
$ make cluster-base
$ make spark-base
$ make spark-master
$ make spark-worker
$ make jupyerlab
```

#### Build at once?
```shell
$ make dependency
```

## Compose Up
```shell
$ make spark-cluster
```

## Compose Down
```shell
$ make spark-cluster-clean
```

## Spark Submit Session
```shell
$ make spark-submit
```
---

## :computer: Web UI
- **JupyterLab** at [localhost:8888](localhost:8888)
- **Spark master** at [localhost:8080](localhost:8080)
- **Spark worker I** at [localhost:8081](localhost:8081)
- **Spark worker II** at [localhost:8082](localhost:8082)
