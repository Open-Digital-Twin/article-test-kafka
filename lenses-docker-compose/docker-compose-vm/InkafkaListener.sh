#! /bin/bash

TOPIC=$1

echo "Listenning to topic ${TOPIC}"
docker exec -i fastdata kafka-console-consumer    --bootstrap-server localhost:9092    --topic ${TOPIC}    --from-beginning
