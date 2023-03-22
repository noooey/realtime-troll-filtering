spark-server:
	sudo docker compose -p spark-cluster -f docker-compose.yaml up

spark-server-clean:
	sudo docker compose -p spark-cluster down -v
	sudo docker rmi -f \
		spark-cluster-data-preprocessor