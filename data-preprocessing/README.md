# Message Consuming on Docker

## Image Build & Run
```shell
# Makefile
spark-server:
	sudo docker compose -p spark-cluster -f docker-compose.yaml

spark-server-clean:
	sudo docker compose -p spark-cluster down -v
```
