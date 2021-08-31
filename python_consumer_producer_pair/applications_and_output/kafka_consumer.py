from kafka import KafkaConsumer
from json import loads, dumps
from itertools import count
import random
from time import sleep
from datetime import datetime
from subprocess import getoutput
from sys import argv, exit
import time
if not len(argv) == 4:
    exit('this program requires 3 arguments, first the topic, then server and the port')

topic = argv[1]
server = argv[2]
port = argv[3]

index = count()

# Create an instance of the Kafka producer
consumer = KafkaConsumer(topic,
                         bootstrap_servers=server+':'+port,
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         group_id='my-group',
                         value_deserializer=lambda x: loads(x.decode('utf-8'))
                        )

with open('output_consumer', 'w', buffering=1) as redf:

    print("Ctrl+c to Stop")
    # Call the producer.send method with a producer-record
    i = 0
    for message in consumer:
        time = datetime.timestamp(datetime.now())
        contents = {'topic': str(message.topic), 'timestamp': str(time.strftime('%Y/%m/%d %H:%M:%S.%f', time.gmtime(int(message.timestamp)/1000.))), 'value': str(message.value)} 
        if not contents:
            break
        if i == 0:
            first_message_timestamp = message.timestamp
            i = 1
        # stuff = getoutput('docker stats 7b0ab8128574 --format \"{{.Name}},{{.CPUPerc}},{{.MemUsage}}\" --no-stream')
        # docker takes waaay too long to do this stuff
        time_passage = int(message.timestamp) - int(first_message_timestamp)
        redf.write(f'{message.topic},{message.timestamp},{message.value},{time_passage} \n')
        print(f'{contents},{time}')
