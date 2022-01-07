from os import write
from kafka import KafkaConsumer
from json import loads
from itertools import count
from datetime import datetime
from sys import argv, exit, getsizeof
import time
import argparse
import objsize
parser = argparse.ArgumentParser()

parser.add_argument("-t", "--topic", help="kafka topic to get the messages", nargs='?', const='topic', type=str, default='topic')
parser.add_argument("-s", "--server", help="kafka container to connect", nargs='?', const='kafka_1', type=str, default='kafka_1')
parser.add_argument("-p", "--server_port", help="Port where the kafka container listens", nargs='?', const='9091', type=str, default='9091')
parser.add_argument("-n", "--n_messages", help="Sends N messages", nargs='?', const=1000, type=int, default=1000)
parser.add_argument("-o", "--output_every", help="Outputs to file every X messages received, and at the end", nargs='?', const=100, type=int, default=100)

args = parser.parse_args()

topic = args.topic
server = args.server
port = args.server_port
number_of_messages = args.n_messages

# Create an instance of the Kafka producer
consumer = KafkaConsumer(topic,
                         bootstrap_servers=server+':'+port,
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         group_id='my-group',
                         value_deserializer=lambda x: loads(x.decode('utf-8'))
                        )
write_buffer = []

with open('output_consumer', 'w', buffering=1) as redf:
    redf.write('topic, kafka_timestamp, message_value, message_producer_time, message_consumer_time, consumer_produtor_latency, time_passed_since_kafka_timestamp_1, size\n')
    print("Ctrl+c to Stop")
    # Call the producer.send method with a producer-record
    counter = count()
    for (index, message) in enumerate(consumer, start=1):
        time = datetime.timestamp(datetime.now())
        message_producer_time = message.value['producer_time']
        consumer_produtor_latency = time - message_producer_time
        
        message_value = message.value['value']
        if index == 0:
            first_message_timestamp = message.timestamp

        time_passage = (message.timestamp - first_message_timestamp)/1000
        contents = f'{message.topic}, {message.timestamp/1000}  , {message_value}          , {message_producer_time}    , {time}    , {consumer_produtor_latency}      ,      {time_passage}                           '
        write_buffer.append(f'{contents}, {str(objsize.get_deep_size(message))} \n')
        
        if index % args.output_every == 0:
            redf.write(write_buffer)
            write_buffer = []
            print(f'message_number: {index}')
        
        if index == (number_of_messages):
            redf.write(write_buffer)
            write_buffer = []
            redf.close()
            exit()
            break
    exit()