from kafka.admin import KafkaAdminClient, NewTopic
from random import randint

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-t", "--topic", help="kafka topic name", nargs='?', const='topic', type=str, default='topic')
parser.add_argument("-s", "--server", help="kafka container to connect", nargs='?', const='kafka_1', type=str, default='kafka_kafka')
parser.add_argument("-p", "--server_port", help="Port where the kafka container listens", nargs='?', const='9091', type=str, default='9094')

args = parser.parse_args()

server_addr = f'{args.server}:{args.server_port}'
print(server_addr)

topic_uid = randint(100000, 999999)
topic_name = f'{args.topic}_{topic_uid}'

admin_client = KafkaAdminClient(
    bootstrap_servers= server_addr, 
    client_id='test'
)

topic_list = []
topic_list.append(NewTopic(name=topic_name, num_partitions=1, replication_factor=1))
admin_client.create_topics(new_topics=topic_list, validate_only=False)

print(f'topic: \'{topic_name}\', created')