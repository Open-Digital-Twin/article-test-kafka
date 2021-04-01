#! /bin/bash

echo ""
echo "Sending a message on the mqtt topic..."	
	docker exec mqtt mosquitto_pub  -m "{\"deviceId\":1,\"value\":31.1,\"region\":\"EMEA\",\"timestamp\":5}" -d -r -t /lenses/sending
