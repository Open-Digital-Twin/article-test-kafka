from random import randint
from os import get_terminal_size
from time import sleep
import subprocess

line_width = get_terminal_size().columns
half_line = int(line_width/2)

def start_consumers(topic_list = [], msg_num = 1000):
    print('\n' + '-' * (half_line - 9)+ ' Starting consumers ' + '-' * (half_line - 8) + '\n')
    
    for consumer in topic_list:
        print(f'From node {consumer["node"]}, started consumer {consumer["consumer"]}')
        cmd_docker = ['docker', f'-H {consumer["node"]}', 'exec', '-d',f'{consumer["consumer"]}']
        cmd_container = cmd_docker + ['python3', 'kafka_consumer.py', '-t', consumer['topic'], '-s', 'kafka_kafka', '-p', '9094', '-n', f'{msg_num}']
        cmd_string = ' '.join([str(item) for item in cmd_container])
        consumer_5 = subprocess.Popen(cmd_string, shell=True)
        sleep(2)

    sleep(1)
    print('\n' + '-' * (half_line - 3) + ' End ' + '-' * (half_line - 2) + '\n')

if __name__ == '__main__':
    from get_all_nodes_names import get_node_names
    node_list = get_node_names()
    from get_container_ids import get_container_structure
    machine_list = get_container_structure(node_list)
    from docker_stats_consumers import get_docker_stats_consumers
    consumer_list = get_docker_stats_consumers(machine_list)
    from create_topics import create_topic_per_consumer
    topic_list = create_topic_per_consumer(consumer_list)
    start_consumers(topic_list)
