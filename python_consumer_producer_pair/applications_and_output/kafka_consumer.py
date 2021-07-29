from kafka import KafkaConsumer
from json import loads, dumps
from itertools import count
import random
from time import sleep
from datetime import datetime
from subprocess import getoutput
from sys import argv, exit

if not len(argv) == 3:
    exit('this program requires 2 arguments, first the port then the topic')

topic = argv[1]
port = argv[2]

index = count()

# Create an instance of the Kafka producer
consumer = KafkaConsumer(topic,
                         bootstrap_servers=['localhost:%s' % port],
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         group_id='my-group',
                         value_deserializer=lambda x: loads(x.decode('utf-8'))
                        )

with open('output_consumer', 'w', buffering=1) as redf:

    print("Ctrl+c to Stop")
    # Call the producer.send method with a producer-record
    for message in consumer:
        now = datetime.now()
        contents = {'message': str(message.value) , 'read_when': str(datetime.timestamp(now)), 'timedelta': str(datetime.timestamp(now) - float(message.value['timestamp'])) } 
        # stuff = getoutput('docker stats 7b0ab8128574 --format \"{{.Name}},{{.CPUPerc}},{{.MemUsage}}\" --no-stream')
        # docker takes waaay too long to do this stuff
        redf.write('stuff' + ',' + contents['timedelta'] + '\n')
        print(contents)


