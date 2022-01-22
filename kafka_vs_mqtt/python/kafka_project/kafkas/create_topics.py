from random import randint
import subprocess

from auxiliaryfunctions.terminal import print_centralized

def create_topic_per_consumer(consumer_list = [], replication = 1, partition = 1, exp_type = 'kafka'):
    print_centralized(' Creating topics ')
    
    topic_list = []
    for consumer in consumer_list:
        print(f'Created topic from {consumer["node"]} of consumer {consumer["consumer"]}')
        topic_name = f'topic_{consumer["node"]}_{consumer["consumer"]}_{randint(111111111,999999999)}'

        if exp_type == 'kafka':
            cmd_docker = ['docker', f'-H {consumer["node"]}', 'exec',f'{consumer["consumer"]}']
            cmd_container = cmd_docker +['python3', 'kafka_topic_creation.py', '-t', topic_name, '-s', 'experiment_kafka', '-p', '9094', '-r', replication, '-n', partition]
            cmd_string = ' '.join([str(item) for item in cmd_container])
            consumer_process = subprocess.run(cmd_string, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines= True)
            print(consumer_process.stdout)
            print(consumer_process.stderr)
            
        topic_list.append({'node': consumer['node'], 'topic':topic_name, 'consumer':consumer['consumer']})
    
    print_centralized(' End ')

    return topic_list

if __name__ == '__main__':
    from networkstructure.nodes import get_node_names
    node_list = get_node_names()
    from networkstructure.containers import get_container_structure
    from consumers.consumer_stats import get_docker_stats_consumers
    machine_list = get_container_structure(node_list)
    consumer_list = get_docker_stats_consumers(machine_list)
    create_topic_per_consumer(consumer_list, replication = 3)
