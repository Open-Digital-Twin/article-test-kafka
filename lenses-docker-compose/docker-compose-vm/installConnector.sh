#! /bin/bash


echo ""
echo "Copying connector files into fastdata..."
	docker cp connectorMQTTsource.properties  fastdata:/
	docker cp connectorMQTTsink.properties  fastdata:/

echo ""
echo "Removing and Starting connector Source... (may have an error warning if its first installation)"
	docker exec -i fastdata connect-cli rm mqttSource
	docker exec -i fastdata connect-cli create mqttSource < connectorMQTTsource.properties

#sleep 1.5

echo ""
echo "Removing and Starting connector Sink... (may have an error warning if its first installation)"
	docker exec -i fastdata connect-cli rm mqttSink	
	docker exec -i fastdata connect-cli create mqttSink < connectorMQTTsink.properties
