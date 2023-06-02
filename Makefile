dependency:
	make -C ./fast-api/ fast-api
	make -C ./kafka-cluster/ kafka-cluster
	make -C ./spark-cluster/ dependency
	make -C ./spark-cluster/ spark-cluster
	make -C ./spark-cluster/ spark-submit

dependency-clean:
	make -C ./youtube-api/ youtube-api-clean
	make -C ./spark-cluster/ spark-cluster-clean
	make -C ./kafka-cluster/ kafka-cluster-clean
	make -C ./fast-api/ fast-api-clean

run:
	make -C ./youtube-api/ youtube-api