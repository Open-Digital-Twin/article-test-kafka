This is just a part of a Digital Twin project at:

It is responsable for the transmission of data from MQTT to Kafka (kafka processes somehow the data) then answers back

So far theres absolutely nothing here, tho.


Now there are two new files

	docker-compose2.yml is just a model file with all the stuff mosquitto/kafka/zookeeper/kafdrop (in case of an empty VM)
	docker-compse.yml has just kafka and zookeeper (the one for the VM)
