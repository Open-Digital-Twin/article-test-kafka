from kafka import KafkaProducer
from json import loads, dumps
import random
from time import sleep
from datetime import datetime
from sys import argv, exit

if not len(argv) == 4:
    exit('this program requires 3 arguments, first the topic, second the server name, and then the port')

topic = argv[1]
server = argv[2]
port = argv[3]

number_of_messages = 1000

# Create an instance of the Kafka producer
producer = KafkaProducer(bootstrap_servers=server+':'+port,
                         value_serializer=lambda x: dumps(x).encode('utf-8')
                        )

# Call the producer.send method with a producer-record
print("Ctrl+c to Stop")
i = 0
while i < number_of_messages:
    data = {'value':str(random.randint(1,999))}
    producer.send(topic, data)
    i += 1
    print(data)
    sleep(1)