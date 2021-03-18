#! /bin/bash
echo "Sending a message on the mqtt topic..."	
	docker exec mqtt mosquitto_pub  -m "{\"deviceId\":1,\"value\":31.1,\"region\":\"EMEA\",\"timestamp\":3}" -d -r -t /lenses/sending

echo ""
echo "Listening a message on the mqtt topic..."
	docker exec mqtt mosquitto_sub -t /lenses/sending
	
