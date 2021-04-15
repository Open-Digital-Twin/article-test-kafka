#! /bin/bash
echo ""
echo "Listening a message on the mqtt topic '/lenses/sending'..."
	docker exec mqtt mosquitto_sub -t /lenses/sending
	
