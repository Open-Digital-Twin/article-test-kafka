from kafka.admin import KafkaAdminClient, NewTopic
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-t", "--topic", help="kafka topic to get the messages", nargs='?', const='topic', type=str, default='topic')
parser.add_argument("-s", "--server", help="kafka container to connect", nargs='?', const='kafka_1', type=str, default='kafka_1')
parser.add_argument("-p", "--server_port", help="Port where the kafka container listens", nargs='?', const='9091', type=str, default='9091')
parser.add_argument("-r", "--replication_factor", help="Topic replication factor", nargs='?', const=1, type=int, default=1)
parser.add_argument("-n", "--n_of_partitions", help="Number of paritions of topic", nargs='?', const=1, type=int, default=1)

args = parser.parse_args()

connection = KafkaAdminClient(bootstrap_servers= f'{args.server}:{args.server_port}')

topic = NewTopic(name= args.topic, num_partitions= args.n_of_partitions, replication_factor= args.replication_factor)
new_topic = connection.create_topics([topic])

print(str(new_topic))

#This SHOULD work
