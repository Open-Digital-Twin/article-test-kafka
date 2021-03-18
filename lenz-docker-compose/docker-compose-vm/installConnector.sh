#! /bin/bash

echo ""
echo "Waiting for stuff for 2sec..."
sleep 2

echo ""
echo "Starting connector Source..."
	docker exec -i fastdata connect-cli create mqttSource < connectorMQTTsource.properties

#sleep 1.5

#echo ""
#echo "Starting connector Sink..."
#	docker exec fastdata connect-cli create mqttSink < connectorMQTTsink.properties
