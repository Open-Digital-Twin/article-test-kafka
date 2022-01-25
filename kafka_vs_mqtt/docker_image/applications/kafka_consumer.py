from kafka import KafkaConsumer
from json import loads
from datetime import datetime
from sys import exit
import time
import argparse
import objsize
parser = argparse.ArgumentParser()

parser.add_argument("-t", "--topic", help="kafka topic to get the messages", nargs='?', const='topic', type=str, default='topic')
parser.add_argument("-s", "--server", help="kafka container to connect", nargs='?', const='experiment_kafka', type=str, default='experiment_kafka')
parser.add_argument("-p", "--server_port", help="Port where the kafka container listens", nargs='?', const='9094', type=str, default='9094')
parser.add_argument("-n", "--n_messages", help="Sends N messages", nargs='?', const=1000, type=int, default=1000)
parser.add_argument("-o", "--output_every", help="Outputs to file every X messages received, and at the end", nargs='?', const=100, type=int, default=100)

args = parser.parse_args()

topic = args.topic
server = args.server
port = args.server_port
number_of_messages = args.n_messages

# Create an instance of the Kafka producer
consumer = KafkaConsumer(
    topic,
    bootstrap_servers = f'{server}:{port}',
    auto_offset_reset = 'earliest',
    enable_auto_commit = True,
    group_id = 'my-group',
    value_deserializer = lambda x: loads(x.decode('utf-8'))
)

write_buffer = []
with open('output_kafka_consumer', 'w', buffering = 1) as redf:
    redf.write('topic,kafka_timestamp,message_value,message_producer_time,message_consumer_time,message_size,total_size\n')
    print("Ctrl+c to Stop")
    # Call the producer.send method with a producer-record
    for (index, message) in enumerate(consumer, start = 1):
        
        current_time = datetime.timestamp(datetime.now())
        producer_time = message.value['producer_time']
        value = message.value['value']
        message_size = objsize.get_deep_size(message.value)
        package_size = objsize.get_deep_size(message)
        kafka_time = message.timestamp/1000
        topic = message.topic

        contents = f'{topic},{kafka_time},{value},{producer_time},{current_time},{message_size},{package_size}'
        write_buffer.append(contents)
        
        if (index % args.output_every == 0):
            for item in write_buffer:
                redf.write("%s\n" % item)
            write_buffer = []
            print(f'message_number: {index}', end = '\r')
        
        if (index == number_of_messages):
            for item in write_buffer:
                redf.write("%s\n" % item)
            write_buffer = []
            redf.close()
            break
    exit()