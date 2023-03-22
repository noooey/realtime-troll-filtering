# Running Kafka Cluste on Docker

## Image Build & Run
```Makefile
# Makefile
kafka-server:
	sudo docker compose -p kafka-cluster -f docker-compose.yaml -d

kafka-server-clean:
	sudo docker compose -p kafka-cluster down -v
```
