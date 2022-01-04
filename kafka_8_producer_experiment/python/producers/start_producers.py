from random import randint
from os import get_terminal_size
import subprocess
from time import sleep

line_width = get_terminal_size().columns
half_line = int(line_width/2)

def start_producers(producer_list = [], topic_list = [], msg_number = 1000, msg_size = 0, msg_delay = 0.01):
    print('\n' + '-' * (half_line - 9)+ ' Starting producers ' + '-' * (half_line - 8) + '\n')
    
    producer_quantity = len(producer_list)
    topic_quantity = len(topic_list)
    producer_per_topic = int(producer_quantity/topic_quantity)

    for topic in topic_list:
        begin = 0
        print(producer_list)
        for producer in producer_list[begin : begin + producer_per_topic]:
            
            cmd_docker = ['docker', f'-H {producer["node"]}', 'exec', '-d',f'{producer["producer"]}']
            print(cmd_docker)
            cmd_container = cmd_docker + ['python3', 'kafka_producer.py', '-t', topic['topic'], '-s', 'kafka_kafka', '-p', '9094', '-n', msg_number, '-d', msg_delay, '-e', msg_size]
            cmd_string = ' '.join([str(item) for item in cmd_container])
            producer_5 = subprocess.Popen(cmd_string, shell=True)

            begin += 1
            print(f'From node {producer["node"]}, started producer {producer["producer"]}, in topic {topic["topic"]}')
    
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
    from start_consumers import start_consumers
    start_consumers(topic_list)
    
    from docker_stats_producers import get_docker_stats_producers
    producer_list = get_docker_stats_producers(machine_list)
    start_producers(producer_list, topic_list)
    sleep(5)
