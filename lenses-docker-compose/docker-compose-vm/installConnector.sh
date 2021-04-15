#! /bin/bash


echo ""
echo "Copying connector files into fastdata..."
	docker cp connectorMQTTsource.properties  fastdata:/
	docker cp connectorMQTTsink.properties  fastdata:/
	
echo "Copying stream app files into fastdata..."
	echo "From main file..."
	docker cp streamApp/streams.examples/target/streams.examples-0.1.jar  fastdata:/


sleep 1.5

echo ""
echo "Removing and Starting connector Source... (may have an error warning if its first installation)"
	docker exec -i fastdata connect-cli rm mqttSource
	docker exec -i fastdata connect-cli create mqttSource < connectorMQTTsource.properties

#sleep 1.5

echo ""
echo "Removing and Starting connector Sink... (may have an error warning if its first installation)"
	docker exec -i fastdata connect-cli rm mqttSink	
	docker exec -i fastdata connect-cli create mqttSink < connectorMQTTsink.properties

#sleep 1.5

echo "Initiating Pipe Processing"
	docker exec -i fastdata kafka-topics --create  --bootstrap-server localhost:9092     --replication-factor 1     --partitions 1     --topic mqtt
	docker exec -i fastdata kafka-topics --create     --bootstrap-server localhost:9092     --replication-factor 1     --partitions 1     --topic mqttOut
	docker exec -i fastdata kafka-run-class -cp /streams.examples-0.1.jar myapps.Pipe
		
#kafka-run-class myapps.Pipe
