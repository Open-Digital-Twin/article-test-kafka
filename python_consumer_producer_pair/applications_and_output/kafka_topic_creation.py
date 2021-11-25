from kafka.admin import KafkaAdminClient, NewTopic
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-t", "--topic", help="kafka topic to get the messages", nargs='?', const='topic', type=str, default='topic')
parser.add_argument("-s", "--server", help="kafka container to connect", nargs='?', const='kafka_1', type=str, default='kafka_1')
parser.add_argument("-p", "--server_port", help="Port where the kafka container listens", nargs='?', const='9091', type=str, default='9091')
parser.add_argument("-n", "--n_messages", help="Sends N messages", nargs='?', const=1000, type=int, default=1000)

args = parser.parse_args()

connection = KafkaAdminClient(bootstrap_servers= f'{args.server}:{args.server_port}')

topic = NewTopic(name= args.topic, num_partitions= 1, replication_factor= 1)
new_topic = connection.create_topics([topic])

print(str(new_topic))

#This SHOULD work
