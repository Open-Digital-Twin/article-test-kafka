from kafka import KafkaProducer
from json import loads, dumps
import random
from time import sleep
from datetime import datetime

#kafka topic to send the message
topic = 'messages'

# Create an instance of the Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:29092',
                         value_serializer=lambda x: dumps(x).encode('utf-8')
                        )

# Call the producer.send method with a producer-record
print("Ctrl+c to Stop")
while True:
    now = datetime.now()
    data = {'value':str(random.randint(1,999)), 'timestamp': str(datetime.timestamp(now))}
    producer.send(topic, data)
    sleep(1)
