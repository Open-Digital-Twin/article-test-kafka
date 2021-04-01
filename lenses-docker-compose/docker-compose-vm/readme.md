#Just run the scripts in this order:

. ./startLenses.sh mqtt
#mqtt is the name of the mqtt container, it can be anything, just remember to edit the connectorMQTTsink/source (at least for now)

#wait till fastdata is initialized (may take a while)

./installConnector

#Then you can open another terminal, or start here
./insertMosquitto.sh mqtt 
#just a quick producer that generates random values and puts in a mosquitto 

#then you can follow the readme in the previous folder do vizualise those things happening.
#end everything with

./endMe.sh
