spark-cluster:
	docker compose -f docker-compose.yaml up

spark-cluster-clean:
	docker compose down -v

spark-submit:
	docker exec -it spark-master /usr/bin/spark-3.3.2-bin-hadoop2/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,org.apache.commons:commons-pool2:2.11.1,org.apache.kafka:kafka-clients:2.5.0,org.apache.spark:spark-streaming-kafka-0-10_2.12:3.3.2 spark-streaming.py