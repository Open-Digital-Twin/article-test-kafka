from time import sleep
from random import randint
import argparse
import subprocess

parser = argparse.ArgumentParser()

from get_container_ids import get_container_structure
from get_all_nodes_names import get_node_names

# Topic Creation
parser.add_argument("-nt", "--new_topic", help="kafka topic to get the messages", nargs='?', const='topic', type=str, default='topic')
parser.add_argument("-ns", "--new_topic_server", help="kafka container to connect", nargs='?', const='kafka_1', type=str, default='kafka_kafka')
parser.add_argument("-np", "--new_topic_server_port", help="Port where the kafka container listens", nargs='?', const='9094', type=str, default='9094')
parser.add_argument("-nr", "--new_topic_replication_factor", help="Topic replication factor", nargs='?', const=1, type=int, default=1)
parser.add_argument("-nn", "--new_topic_n_of_partitions", help="Number of paritions of topic", nargs='?', const=1, type=int, default=1)

# Topic Consumer
parser.add_argument("-ct", "--consumer_topic", help="kafka topic to get the messages", nargs='?', const='topic', type=str, default='topic')
parser.add_argument("-cs", "--consumer_server", help="kafka container to connect", nargs='?', const='kafka_1', type=str, default='kafka_kafka')
parser.add_argument("-cp", "--consumer_server_port", help="Port where the kafka container listens", nargs='?', const='9091', type=str, default='9094')
parser.add_argument("-cn", "--consumer_n_messages", help="Sends N messages", nargs='?', const=1000, type=int, default=1000)

# Topic Producer
parser.add_argument("-pt", "--producer_topic", help="kafka topic to send the messages", nargs='?', const='topic', type=str, default='topic')
parser.add_argument("-ps", "--producer_server", help="kafka container to connect", nargs='?', const='kafka_kafka', type=str, default='kafka_kafka')
parser.add_argument("-pp", "--producer_server_port", help="Port where the kafka container listens", nargs='?', const='9091', type=str, default='9091')
parser.add_argument("-pd", "--producer_delay", help="Waiting time beetween messages", nargs='?', const=0.01, type=float, default=0.01)
parser.add_argument("-pn", "--producer_n_messages", help="Sends N messages", nargs='?', const=1000, type=int, default=1000)
parser.add_argument("-pe", "--producer_entries", help="Entries additional to the original dictionary (makes the message bigger)", nargs='?', const=0, type=int, default=0)

nodes = get_node_names()
containers = get_container_structure(nodes)
#topics = create_topics(containers)
#start_consumers(containers, topics)
#start_producers(containers, topics)

### Start of the actual script
## Topic Creation Step
# Dtwins5 topic
dt5_topic_name = f'dtwins5_{randint(111111, 999999)}'
cmd_docker = ['docker', '-H dtwins5', 'exec', '-d',f'{containers["dtwins5"]["consumer"][0]}']
cmd_container = cmd_docker + ['python3', 'kafka_topic_creation.py', '-t', dt5_topic_name, '-s', 'kafka_kafka', '-p', '9094', '-r', '2']
cmd_string = ' '.join([str(item) for item in cmd_container])
consumer = subprocess.run(cmd_string, shell=True)
# Dtwins6 topic
dt6_topic_name = f'dtwins6_{randint(111111, 999999)}'
cmd_docker = ['docker', '-H dtwins6', 'exec', '-d',f'{containers["dtwins6"]["consumer"][0]}']
cmd_container = cmd_docker + ['python3', 'kafka_topic_creation.py', '-t', dt6_topic_name, '-s', 'kafka_kafka', '-p', '9094', '-r', '2']
cmd_string = ' '.join([str(item) for item in cmd_container])
consumer = subprocess.run(cmd_string, shell=True)
# Dtwins7 topic
dt7_topic_name = f'dtwins7_{randint(111111, 999999)}'
cmd_docker = ['docker', '-H dtwins7', 'exec', '-d',f'{containers["dtwins7"]["consumer"][0]}']
cmd_container = cmd_docker + ['python3', 'kafka_topic_creation.py', '-t', dt7_topic_name, '-s', 'kafka_kafka', '-p', '9094', '-r', '2']
cmd_string = ' '.join([str(item) for item in cmd_container])
consumer = subprocess.run(cmd_string, shell=True)

## Initializing Consumers
# Dtwins5 consumer
cmd_docker = ['docker', '-H dtwins5', 'exec', '-d',f'{containers["dtwins5"]["consumer"][0]}']
cmd_container = cmd_docker + ['python3', 'kafka_consumer.py', '-t', dt5_topic_name, '-s', 'kafka_kafka', '-p', '9094', '-n', '1000']
cmd_string = ' '.join([str(item) for item in cmd_container])
consumer_5 = subprocess.Popen(cmd_string, shell=True)
# Dtwins6 consumer
cmd_docker = ['docker', '-H dtwins6', 'exec', '-d',f'{containers["dtwins6"]["consumer"][0]}']
cmd_container = cmd_docker + ['python3', 'kafka_consumer.py', '-t', dt6_topic_name, '-s', 'kafka_kafka', '-p', '9094', '-n', '1000']
cmd_string = ' '.join([str(item) for item in cmd_container])
consumer_6 = subprocess.Popen(cmd_string, shell=True)
# Dtwins7 consumer
cmd_docker = ['docker', '-H dtwins7', 'exec', '-d',f'{containers["dtwins7"]["consumer"][0]}']
cmd_container = cmd_docker + ['python3', 'kafka_consumer.py', '-t', dt7_topic_name, '-s', 'kafka_kafka', '-p', '9094', '-n', '1000']
cmd_string = ' '.join([str(item) for item in cmd_container])
consumer_7 = subprocess.Popen(cmd_string, shell=True)

#waiting for consumer to stabilize
sleep(5)

##Collecting kafka containers stats
# Dtwins2
cmd_docker = ['docker', '-H dtwins2', 'stats', containers["dtwins2"]["kafka"][0] , '--format', '"{{.Container}}, {{.CPUPerc}}, {{.MemUsage}}, {{.NetIO}}"']
docker_stats_2 = subprocess.Popen(cmd_docker, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
# Dtwins3
cmd_docker = ['docker', '-H dtwins3', 'stats', containers["dtwins3"]["kafka"][0] , '--format', '"{{.Container}}, {{.CPUPerc}}, {{.MemUsage}}, {{.NetIO}}"']
docker_stats_3 = subprocess.Popen(cmd_docker, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
# Dtwins4
cmd_docker = ['docker', '-H dtwins4', 'stats', containers["dtwins4"]["kafka"][0] , '--format', '"{{.Container}}, {{.CPUPerc}}, {{.MemUsage}}, {{.NetIO}}"']
docker_stats_4 = subprocess.Popen(cmd_docker, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)


## Initializing Producers
# Dtwins5 producer
cmd_docker = ['docker', '-H dtwins5', 'exec', '-d',f'{containers["dtwins5"]["producer"][0]}']
cmd_container = cmd_docker + ['python3', 'kafka_producer.py', '-t', dt5_topic_name, '-s', 'kafka_kafka', '-p', '9094', '-n', '1000', '-d', '0.01']
cmd_string = ' '.join([str(item) for item in cmd_container])
producer_5 = subprocess.Popen(cmd_string, shell=True)
print('started dtwins5 producer')
# Dtwins6 producer
cmd_docker = ['docker', '-H dtwins6', 'exec', '-d',f'{containers["dtwins6"]["producer"][0]}']
cmd_container = cmd_docker + ['python3', 'kafka_producer.py', '-t', dt6_topic_name, '-s', 'kafka_kafka', '-p', '9094', '-n', '1000', '-d', '0.01']
cmd_string = ' '.join([str(item) for item in cmd_container])
producer_6 = subprocess.Popen(cmd_string, shell=True)
print('started dtwins6 producer')
# Dtwins7 producer
cmd_docker = ['docker', '-H dtwins7', 'exec', '-d',f'{containers["dtwins7"]["producer"][0]}']
cmd_container = cmd_docker + ['python3', 'kafka_producer.py', '-t', dt7_topic_name, '-s', 'kafka_kafka', '-p', '9094', '-n', '1000', '-d', '0.01']
cmd_string = ' '.join([str(item) for item in cmd_container])
producer_7 = subprocess.Popen(cmd_string, shell=True)
print('started dtwins7 producer')

## Creating experiment folder
exp_number = randint(111111111,999999999)
exp_folder = f'~/experiment_{exp_number}'
cmd_exp = ['mkdir', exp_folder]
cmd_string = ' '.join([str(item) for item in cmd_exp])
consumer = subprocess.run(cmd_string, shell=True)

## Waiting for the messages to be sent
print(f'Experiment: {exp_number} \nWaiting for completion...')
producer_5.wait()
producer_6.wait()
producer_7.wait()

## Waiting for the messages to be received
consumer_5.wait()
consumer_6.wait()
consumer_7.wait()

sleep(20)

## Copying from output to folder
app_folder = '/usr/src/app'
# Coping from Dtwins5 consumer
cmd_docker = ['docker', '-H dtwins5', 'cp', f'{containers["dtwins5"]["consumer"][0]}:{app_folder}/output_consumer', f'{exp_folder}/output_{dt5_topic_name}']
cmd_string = ' '.join([str(item) for item in cmd_docker])
consumer = subprocess.run(cmd_string, shell=True)
# Coping from Dtwins6 consumer
cmd_docker = ['docker', '-H dtwins6', 'cp', f'{containers["dtwins6"]["consumer"][0]}:{app_folder}/output_consumer', f'{exp_folder}/output_{dt6_topic_name}']
cmd_string = ' '.join([str(item) for item in cmd_docker])
consumer = subprocess.run(cmd_string, shell=True)
# Coping from Dtwins7 consumer
cmd_docker = ['docker', '-H dtwins7', 'cp', f'{containers["dtwins7"]["consumer"][0]}:{app_folder}/output_consumer', f'{exp_folder}/output_{dt7_topic_name}']
cmd_string = ' '.join([str(item) for item in cmd_docker])
consumer = subprocess.run(cmd_string, shell=True)

##Saving docker stats
print('Saving docker stats of the experiment..')
home_path = '/home/adbarros/'
exp_folder = exp_folder.split('~/')[1]
print(exp_folder)
# Dtwins2 kafka 
docker_stats_2.kill()
stats_stdout , stats_stderr = docker_stats_2.communicate()
with open(f'{home_path}/{exp_folder}/docker_stats_2.txt', 'w+') as f:
    f.write(stats_stdout)
## Dtwins3 kafka 
docker_stats_3.kill()
stats_stdout , stats_stderr = docker_stats_3.communicate()
with open(f'{home_path}/{exp_folder}/docker_stats_3.txt', 'w+') as f:
        f.write(stats_stdout)
# Dtwins4 kafka 
docker_stats_4.kill()
stats_stdout , stats_stderr = docker_stats_4.communicate()
with open(f'{home_path}/{exp_folder}/docker_stats_4.txt', 'w+') as f:
        f.write(stats_stdout)

print(f'Experiment: {exp_number} \nEnd!')

