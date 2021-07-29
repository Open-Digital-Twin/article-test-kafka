from json import loads, dumps
import random
from time import sleep
from datetime import datetime
from sys import argv, exit

if not len(argv) == 3:
    exit('this program requires 2 arguments, first the port then the topic')

topic = argv[1]
port = argv[2]
    

#kafka topic to send the message
topic = 'messages'

# Create an instance of the Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:%s' % port,
                         value_serializer=lambda x: dumps(x).encode('utf-8')
                        )

# Call the producer.send method with a producer-record
print("Ctrl+c to Stop")
while True:
    now = datetime.now()
    data = {'value':str(random.randint(1,999)), 'timestamp': str(datetime.timestamp(now))}
    producer.send(topic, data)
    sleep(1)
