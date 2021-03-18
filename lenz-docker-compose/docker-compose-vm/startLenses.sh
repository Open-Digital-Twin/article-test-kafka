#! /bin/bash

echo ""
echo "Setting connector global variable...(this is the container_name for the mqtt)"
	export CONNECTOR=mqtt

echo ""
echo "Starting fast data and mqtt..."
	docker-compose up -d

sleep 1.5

echo ""
echo "Copying connector files into fastdata..."
	docker cp connectorMQTTsource.properties  fastdata:/
	docker cp connectorMQTTsink.properties  fastdata:/


