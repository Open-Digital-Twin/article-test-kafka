#! /bin/bash
echo ""
echo "Listening a message on the mqtt topic '/lenses/return'..."
	docker exec mqtt mosquitto_sub -t /lenses/return
	
