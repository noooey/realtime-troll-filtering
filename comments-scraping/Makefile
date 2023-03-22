api-server:
	sudo docker compose -p api-server -f docker-compose.yaml up

api-server-clean:
	sudo docker compose -p api-server down -v
	sudo docker rmi -f \
		api-server-comments-scraper