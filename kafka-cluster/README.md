# Running Kafka Cluster on Docker

## Image Build & Run
```Makefile
kafka-server:
	sudo docker compose -p kafka-cluster -f docker-compose.yaml -d up

kafka-server-clean:
	sudo docker compose -p kafka-cluster down -v
```
