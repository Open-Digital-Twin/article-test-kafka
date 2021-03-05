To begin -> 
	
	export CONNECTOR=mqtt
	
	docker-compose up -d mqtt (in the folder made with compses for the vm, there is no mqtt on the compose)
	
		Also look at this:
			
			To see what network(s) your container is on, assuming your container is called c1:
			$ docker inspect c1 -f "{{json .NetworkSettings.Networks }}"

			To disconnect your container from the first network (assuming your first network is called test-net):
			$ docker network disconnect test-net c1

			Then to reconnect it to another network (assuming it's called test-net-2):
			$ docker network connect test-net-2 c1

			To check if two containers (or more) are on a network together:
			$ docker network inspect test-net -f "{{json .Containers
		Containers NEED to be in the same network

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

