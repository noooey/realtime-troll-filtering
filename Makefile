dependency:
	make -C ./kafka-cluster/ kafka-cluster
	make -C ./spark-cluster/ spark-cluster
	make -C ./spark-client/ spark-client
	make -C ./youtube-api/ youtube-api

dependency-clean:
	make -C ./youtube-api/ youtube-api-clean
	make -C ./spark-client/ spark-client-clean
	make -C ./spark-cluster/ spark-cluster-clean
	make -C ./kafka-cluster/ kafka-cluster-clean

all-server:
	make dependency

all-server-clean:
	make dependency-clean