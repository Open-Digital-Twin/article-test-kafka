from auxiliaryfunctions.terminal import print_centralized
from time import sleep
import subprocess

def start_consumers(topic_list = [], msg_num = 1000):
    print_centralized(' Starting consumers ')
    
    for consumer in topic_list:
        print(f'From node {consumer["node"]}, started consumer {consumer["consumer"]}')
        cmd_docker = ['docker', f'-H {consumer["node"]}', 'exec', '-d',f'{consumer["consumer"]}']
        cmd_container = cmd_docker + ['python3', 'kafka_consumer.py', '-t', consumer['topic'], '-s', 'kafka_kafka', '-p', '9094', '-n', f'{msg_num}']
        cmd_string = ' '.join([str(item) for item in cmd_container])
        consumer_5 = subprocess.Popen(cmd_string, shell=True)
        sleep(2)

    sleep(1)
    print_centralized(' End ')

if __name__ == '__main__':
    from networkstructure.nodes import get_node_names
    node_list = get_node_names()
    from networkstructure.containers import get_container_structure
    machine_list = get_container_structure(node_list)
    from consumers.consumer_stats import get_docker_stats_consumers
    consumer_list = get_docker_stats_consumers(machine_list)
    from kafkas.create_topics import create_topic_per_consumer
    topic_list = create_topic_per_consumer(consumer_list)
    start_consumers(topic_list)
