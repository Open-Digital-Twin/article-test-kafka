from kafka import KafkaConsumer
from json import loads, dumps
from itertools import count
import random
from time import sleep
from datetime import datetime
from subprocess import getoutput
from sys import argv, exit, getsizeof
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
    redf.write('topic, kafka_timestamp, message_value, message_producer_time, message_consumer_time, consumer_produtor_latency, time_passed_since_kafka_timestamp_1, size\n')
    print("Ctrl+c to Stop")
    # Call the producer.send method with a producer-record
    i = 0
    for message in consumer:
        time = datetime.timestamp(datetime.now())
        message_value = message.value['value']
        message_producer_time = message.value['producer_time']

        if i == 0:
            first_message_timestamp = message.timestamp

        time_passage = (message.timestamp - first_message_timestamp)/1000
        consumer_produtor_latency = time - message_producer_time
        contents = f'{message.topic}, {message.timestamp/1000}  , {message_value}          , {message_producer_time}    , {time}    , {consumer_produtor_latency}      ,      {time_passage}                           '
        redf.write(f'{contents}, {str(getsizeof(message))} \n')
        print(contents)
        i += 1
        if i == 999:
            redf.close()
            exit()
            break
    exit()
exit()
