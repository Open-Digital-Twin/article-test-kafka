import subprocess
from time import sleep
from auxiliaryfunctions.terminal import print_centralized

def start_producers(producer_list = [], topic_list = [], msg_number = 1000, msg_size = 0, msg_delay = 0.01, exp_type = 'kafka', limit_conn = True, conn_limit = 1):
    print_centralized(' Starting producers ')
       
    for topic in topic_list:
        topic['connected_prod'] = 0 

    for topic in topic_list:
        print(producer_list)
        for producer in producer_list:
            if producer['node'] == topic['node'] and (limit_conn is False or topic['connected_prod'] <= conn_limit):
                topic['connected_prod'] += 1

                cmd_docker = ['docker', f'-H {producer["node"]}', 'exec', '-d',f'{producer["producer"]}']
                print(cmd_docker)
                
                if (exp_type == 'kafka'):
                    cmd_container = cmd_docker + ['python3', f'{exp_type}_producer.py', '-t', topic['topic'], '-s', f'experiment_{exp_type}', '-p', '9094', '-n', msg_number, '-d', msg_delay, '-e', msg_size]
                else:
                    cmd_container = cmd_docker + ['python3', f'{exp_type}_producer.py', '-t', topic['topic'], '-s', f'experiment_{exp_type}', '-p', 1883, '-n', msg_number, '-d', msg_delay, '-e', msg_size]
                
                cmd_string = ' '.join([str(item) for item in cmd_container])
                subprocess.Popen(cmd_string, shell=True)

                print(f'From node {producer["node"]}, started producer {producer["producer"]}, in topic {topic["topic"]}')

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
    from consumers.call_consumer import start_consumers
    start_consumers(topic_list)
    
    from producers.producer_stats import get_docker_stats_producers
    producer_list = get_docker_stats_producers(machine_list)
    start_producers(producer_list, topic_list)
    sleep(5)
