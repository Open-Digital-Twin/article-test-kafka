#! /bin/bash

TOPIC=$1

echo "Listenning to topic ${TOPIC}"
docker exec -i fastdata kafka-console-consumer --bootstrap-server localhost:9092 --topic ${TOPIC} --from-beginning --formatter kafka.tools.DefaultMessageFormatter --property print.key=true --property print.value=true --property key.deserializer=org.apache.kafka.common.serialization.StringDeserializer --property value.deserializer=org.apache.kafka.common.serialization.LongDeserializer
