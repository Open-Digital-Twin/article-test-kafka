#! /bin/bash

TOPIC=$1

echo "Starting producer on topic ${TOPIC}"
docker exec -i fastdata kafka-console-producer --topic ${TOPIC} --bootstrap-server localhost:9092
