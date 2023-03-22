# Running Kafka Cluste on Docker

## Image Build & Run
```shell
# Makefile
kafka-server:
	sudo docker compose -p kafka-cluster -f docker-compose.yaml

kafka-server-clean:
	sudo docker compose -p kafka-cluster down -v
```
