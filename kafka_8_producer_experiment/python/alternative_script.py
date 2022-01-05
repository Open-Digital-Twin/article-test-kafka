from time import sleep

from graphics.stats_reader import create_stats_graph
from graphics.output_reader import create_message_graph
from networkstructure import nodes, containers
from exportfiles import cloud, compact, results
from consumers import consumer_stats, call_consumer
from producers import producer_stats, start_producers
from kafkas import create_topics, kafka_stats

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--n_messages', help='Number of messages sent per producer', nargs = '?', const = 1000, type = int, default = 1000)
parser.add_argument('-d', '--delay', help='Delay between messages on the producers', nargs = '?', const = 0.01, type = int, default = 0.01)
parser.add_argument('-s', '--message_size', help='Increments message size in chunks of aprox 69 bytes', nargs = '?', const = 0, type = int, default = 0)
parser.add_argument('-r', '--replication', help='Replication factor per topic', nargs = '?', const = 1, type = int, default = 1)
parser.add_argument('-p', '--partition', help='Number of partitions per topic', nargs = '?', const = 1, type = int, default = 1)
args = parser.parse_args()

experiment_number = results.create_experiment_folder()
node_list = nodes.get_node_names()
machine_list = containers.get_container_structure(node_list, experiment_number)

kafka_dict = kafka_stats.get_docker_stats_kafkas(machine_list)
consumer_list = consumer_stats.get_docker_stats_consumers(machine_list)
producer_list = producer_stats.get_docker_stats_producers(machine_list)
topic_list = create_topics.create_topic_per_consumer(consumer_list, args.replication, args.partition)

msgs_per_topic = int(len(producer_list) / len(consumer_list)) * args.n_messages

call_consumer.start_consumers(topic_list, msgs_per_topic)
sleep(7)
start_producers.start_producers(producer_list, topic_list, args.n_messages, args.message_size, args.delay)

consumer_stats.is_experiment_finished()

stats_files = kafka_stats.save_docker_stats_kafkas(kafka_dict, experiment_number)
for file_ in stats_files:
    print(f'Getting graph for stats file {file_}')
    create_stats_graph(experiment_number, file_, save_image= f'{file_}.svg')

output_files = results.export_output_files(consumer_list, experiment_number)
for file_ in output_files:
    print(f'Getting graph for output file {file_}')
    create_message_graph(experiment_number, file_, save_image= f'{file_}.svg')

tar_filepath = compact.tar_experiment_dir(experiment_number)
cloud.gdrive_upload(tar_filepath)
