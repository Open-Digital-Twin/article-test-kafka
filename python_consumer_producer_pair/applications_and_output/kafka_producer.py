from kafka import KafkaProducer
from json import dumps
import random
from time import sleep
from datetime import datetime
from sys import getsizeof
import argparse
import objsize

parser = argparse.ArgumentParser()

parser.add_argument("-t", "--topic", help="kafka topic to send the messages", nargs='?', const='topic', type=str, default='topic')
parser.add_argument("-s", "--server", help="kafka container to connect", nargs='?', const='kafka_1', type=str, default='kafka_1')
parser.add_argument("-p", "--server_port", help="Port where the kafka container listens", nargs='?', const='9091', type=str, default='9091')
parser.add_argument("-d", "--delay", help="Waiting time beetween messages", nargs='?', const=0.0001, type=float, default=0.0001)
parser.add_argument("-n", "--n_messages", help="Sends N messages", nargs='?', const=1000, type=int, default=1000)
parser.add_argument("-e", "--entries", help="Entries additional to the original dictionary (makes the message bigger)", nargs='?', const=0, type=int, default=0)

args = parser.parse_args()

topic = args.topic
server = args.server
port = args.server_port
delay = args.delay
number_of_messages = args.n_messages

# Create an instance of the Kafka producer
producer = KafkaProducer(bootstrap_servers=server+':'+port,
                         value_serializer=lambda x: dumps(x).encode('utf-8')
                        )

data = {}

for i in range(1, (args.entries) + 1):
    data[f'{i}'] = 'justAfixedSizeString'

# Call the producer.send method with a producer-record
print("Ctrl+c to Stop")
i = 0
for i in range(number_of_messages):
    data['value'] = str(random.randint(100,999))
    data['producer_time'] = datetime.timestamp(datetime.now())
    producer.send(topic, data)
    #print(f'data: {data}, size:{objsize.get_deep_size(data)}')
    print(f'message_number: {i}')
    sleep(delay)