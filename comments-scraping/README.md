# Youtube Streaming Comments Scraping on Docker

## Image Build & Run
```shell
# Makefile
api-server:
	sudo docker compose -p api-server -f docker-compose.yaml

api-server-clean:
	sudo docker compose -p api-server down -v
```
