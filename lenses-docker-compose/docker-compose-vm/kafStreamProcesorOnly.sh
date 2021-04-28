#! /bin/bash

echo "Copying stream app files into fastdata..."
	echo "From main file..."
	docker cp streamApp/streams.examples/target/streams.examples-0.1.jar  fastdata:/

#sleep 1.5

echo "Initiating Pipe Processing"
	docker exec -i fastdata kafka-topics --delete --bootstrap-server localhost:9092 --topic mqtt 
	docker exec -i fastdata kafka-topics --delete --bootstrap-server localhost:9092 --topic mqttOut	
	docker exec -i fastdata kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic mqtt
	docker exec -i fastdata kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic mqttOut
	docker exec -i fastdata kafka-run-class -cp /streams.examples-0.1.jar myapps.Pipe
