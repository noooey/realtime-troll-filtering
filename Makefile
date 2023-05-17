dependency:
	make -C ./kafka-cluster/ kafka-cluster
	make -C ./fast-api/ fast-api
	make -C ./spark-cluster/ spark-cluster
	make -C ./youtube-api/ youtube-api

dependency-clean:
	make -C ./youtube-api/ youtube-api-clean
	make -C ./spark-cluster/ spark-cluster-clean
	make -C ./fast-api/ fast-api-clean
	make -C ./kafka-cluster/ kafka-cluster-clean