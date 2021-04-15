#! /bin/bash
temp=""
export CONNECTOR=$1
	
	for i in $(seq 1 9)
	do
 		rNum=$RANDOM
 		# Append 0's for random numbers smaller than 100
  		while [ ${#rNum} -lt 3 ]
  		do 
    		rNum=${rNum}0
  		done
  		
  		# Construct random temperature value from first 3 digits of random number
  		temp="`echo $rNum|cut -c 1`.`echo $rNum|cut -c 2-3`"
  		
		docker exec -ti ${CONNECTOR}  mosquitto_pub -u producer -m "{\"value\":\"${temp}\"}" -d -r -t /lenses/sending
	done
