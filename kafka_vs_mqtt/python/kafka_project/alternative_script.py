from multiprocessing import synchronize
from platform import machine
from time import sleep

from graphics.stats_reader import create_stats_graph
from graphics.output_reader import create_message_graph
from networkstructure import nodes, containers
from exportfiles import cloud, compact, results
from consumers import consumer_stats, call_consumer
from producers import producer_stats, start_producers
from kafkas import create_topics, kafka_stats
from graphics.sync import sanitize_docker_stats

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--n_messages', help='Number of messages sent per producer', nargs = '?', const = 1000, type = int, default = 1000)
parser.add_argument('-d', '--delay', help='Delay between messages on the producers', nargs = '?', const = 0.01, type = float, default = 0.01)
parser.add_argument('-pd', '--producer_delay', help='Waiting time beeting starting each producer', nargs = '?', const = 30, type = int, default = 30)
parser.add_argument('-s', '--message_size', help='Increments message size in chunks of aprox 69 bytes', nargs = '?', const = 0, type = int, default = 0)
parser.add_argument('-r', '--replication', help='Replication factor per topic', nargs = '?', const = 1, type = int, default = 1)
parser.add_argument('-p', '--partition', help='Number of partitions per topic', nargs = '?', const = 1, type = int, default = 1)
parser.add_argument('-c', '--clear_msg_out', help='Clears csv files after the experiment (helpful if there are too many messages)', nargs = '?', const = 'false', type = str, default = 'false')
parser.add_argument('-t', '--experiment_type', help='Which experiment type to do (kafka or mqtt)', nargs='?', const = 'kafka', type = str, default = 'kafka')
args = parser.parse_args()

home_dir = '/home/adbarros/'

if (not args.experiment_type in ('kafka', 'mqtt')):
    print('Invalid experiment typing, must be either "kafka" or "mqtt"')
    exit()

experiment_number = results.create_experiment_folder(exp_type=args.experiment_type)
node_list = nodes.get_node_names()
machine_list = containers.get_container_structure(node_list, experiment_number, exp_type=args.experiment_type)

node_dict, stats_files = kafka_stats.docker_stats_to_file(machine_list, exp_type=args.experiment_type, exp_number=experiment_number)
consumer_list, consumer_file_list, consumer_stats_dict = consumer_stats.get_docker_stats_consumers(machine_list, exp_type=args.experiment_type, exp_number=experiment_number)
producer_list, producer_file_list, producer_stats_dict = producer_stats.get_docker_stats_producers(machine_list, exp_type=args.experiment_type, exp_number=experiment_number)

topic_list = create_topics.create_topic_per_consumer(consumer_list, args.replication, args.partition, exp_type = args.experiment_type)

number_of_processes = consumer_stats.processes_running(consumer_list)
print(number_of_processes)
number_of_producers = len(producer_list)
number_of_consumers = len(consumer_list)

msgs_per_topic = int(number_of_producers / number_of_consumers) * args.n_messages

call_consumer.start_consumers(topic_list, msgs_per_topic, exp_type=args.experiment_type)
sleep(7)
starting_order = start_producers.start_producers(producer_list, topic_list, args.n_messages, args.message_size, args.delay, exp_type=args.experiment_type, wait_between=args.producer_delay)

# this function is slower, but can be useful if there is some problem with the experiment, since it opens the file and reads the lines
# consumer_stats.is_experiment_finished(consumer_list, msgs_per_topic)
print('In case of crash or missing messages, you can skip this loop with ctrl-c, and the program proceeds as usual\n\n\n')
try:
    while True:
        sleep(2)
        current_number = consumer_stats.processes_running(consumer_list)
        if current_number == number_of_processes:
            print('All done!')
            break
        for current_value in current_number: # kinda convoluted, but updates to V, if the consumer is finished
            for initial_value in number_of_processes:
                if current_value == initial_value:
                    current_value[next(iter(current_value))] = 'V'

        print(current_number, end = '\033[A\033[A\033[A\r') # '\033[A' returns a line on linux terminal, and \r returns to the start of line
        # so this goes up 3 lines, and goes to the start of the line, to overwrite the text
        sleep(1)
except KeyboardInterrupt:
    pass

sleep(5)
all_docker_stats_listeners = {**node_dict, **producer_stats_dict, **consumer_stats_dict}

kafka_stats.close_monitoring(all_docker_stats_listeners)
output_files = results.export_output_files(consumer_list, experiment_number, exp_type=args.experiment_type)

producer_consumer_file_list = producer_file_list + consumer_file_list
results.get_synced_message_latency_average(starting_order, output_files, args.producer_delay, experiment_number, '/home/adbarros/', args.experiment_type, args.clear_msg_out)
# machine_total_usage_files = results.get_usage_per_docker_machine(machine_list, producer_consumer_file_list, experiment_number, home_dir, args.experiment_type)

for file_ in stats_files + producer_consumer_file_list:
    print(f'Getting graph for stats file {file_}')
    try:
        sanitize_docker_stats(file_, experiment_number, exp_type=args.experiment_type, home_dir='/home/adbarros/')
        create_stats_graph(experiment_number, file_, save_image= f'{file_}.svg', exp_type=args.experiment_type, clear_csv=args.clear_msg_out)
    except Exception as e:
        print(str(e))

output_files.append('output_docker_complete')

for file_ in output_files:
    print(f'Getting graph for output file {file_}')
    try:
        create_message_graph(experiment_number, file_, save_image= f'{file_}.svg', clear_csv=args.clear_msg_out, exp_type=args.experiment_type)
    except Exception as e:
        print(str(e))

tar_filepath = compact.tar_experiment_dir(experiment_number, exp_type=args.experiment_type)
cloud.gdrive_upload(tar_filepath)
