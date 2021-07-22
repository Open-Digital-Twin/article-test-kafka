from kafka import KafkaConsumer
from json import loads, dumps
from itertools import count
import random
from time import sleep
from datetime import datetime


#kafka topic to read the messages
topic = 'messages'

index = count()

# Create an instance of the Kafka producer
consumer = KafkaConsumer(topic,
                         bootstrap_servers=['localhost:29092'],
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         group_id='my-group',
                         value_deserializer=lambda x: loads(x.decode('utf-8'))
                        )

with open('output_consumer', 'w', buffering=1) as redf:

    redf.write('x_value,delay\n')

    print("Ctrl+c to Stop")
    # Call the producer.send method with a producer-record
    for message in consumer:
        now = datetime.now()
        contents = {'message': str(message.value) , 'read_when': str(datetime.timestamp(now)), 'timedelta': str(datetime.timestamp(now) - float(message.value['timestamp'])) } 
        redf.write(str(next(index)) + ',' + contents['timedelta'] + '\n')
        print(contents)


