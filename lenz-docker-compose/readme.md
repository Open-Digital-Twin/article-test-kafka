To begin -> 
	
	export CONNECTOR=mqtt
	
	docker-compose up -d mqtt

Put connectors on lenses -=-=-=--=-
	
	docker cp /pathToTheFile/connectorMQTTsource.properties  fastdata:/CanbeInAfolderOrNot

Insert and read mosquitto -=-=-=-=-=-=-

	docker exec -ti mqtt  mosquitto_pub  -m "{\"deviceId\":1,\"value\":31.1,\"region\":\"EMEA\",\"timestamp\":3}" -d -r -t /lenses/sending
	docker exec -ti mqtt  mosquitto_sub  -t /lenses/return


Start Kafka consumer on lenses pack -=-=-=-=-=-=-=-=-

	kafka-avro-console-consumer    --bootstrap-server localhost:9092    --topic mqtt    --from-beginning


Connect cli dealings (after doing "docker exec -ti fastdata /bin/sh")=-=-=-=--=

	connect-cli create mqttSource < connectorMQTTsource.properties
	connect-cli status mqttSource
	connect-cli rm mqttSource

