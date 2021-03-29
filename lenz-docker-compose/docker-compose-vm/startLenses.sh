#! /bin/bash

echo ""
echo "Setting connector global variable...(this is the container_name for the mqtt)"
	export CONNECTOR=$1
	
echo ""
echo "Starting fast data and mqtt..."
	docker-compose up -d

sleep 1.5

echo ""
	docker logs fastdata
echo ""
