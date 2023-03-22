dependency:
	make -C ./kafka-cluster/ kafka-server
	make -C ./data-preprocessing/ spark-server
	make -C ./comments-scraping/ api-server

dependency-clean:
	make -C ./comments-scraping/ api-server-clean
	make -C ./data-preprocessing/ spark-server-clean
	make -C ./kafka-cluster/ kafka-server-clean

all-server:
	make dependency

all-server-clean:
	make dependency-clean