#! /bin/bash

# this is unnecessary since its only fastdata that is being started, no mqtt broker, but its to make the warning not appear
export CONNECTOR=mqtt
# because im to lazy to change the yml, you could you just have to locate there something that uses the variable connector and erase

echo "Starting fast data .."
docker-compose -f fastdataOnly.yml up -d

sleep 1.5

echo ""
	docker logs fastdata
echo ""

