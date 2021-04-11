This is just a part of a Digital Twin project is responsable for the transmission of data from MQTT to Kafka (kafka processes somehow the data) then answers back

There is another readme inside the folder 'lenses-docker-compose'. With the step by step.

Ok so, now we have a connector from mqtt, and a stream processor in java implemented. All of this is in
/lenses-docker-compose/docker-compose-vm

All you need to do run the scripts in this order

	./startLenses.sh mqtt
	 >> wait for the startup that can last up to 3 minutes	

	./installConectors.sh
	 >> Now this terminal will be busy with the stream processor, so Start another terminal.	 

	./insertMosquitto.sh
	 >> our "producer"
	 
	 

Then, do
		docker exec -it fastdata /bin/sh
		kafka-avro-console-consumer    --bootstrap-server localhost:9092    --topic mqtt    --from-beginning
		
		This to check your mqtt msgs on the topic mqtt
		
		
		kafka-avro-console-consumer    --bootstrap-server localhost:9092    --topic mqttOut    --from-beginning
		
		To check your mqtt msgs after passing through the processor
		
		
