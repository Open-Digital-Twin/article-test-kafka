import subprocess
from time import sleep
from auxiliaryfunctions.terminal import print_centralized

def get_docker_stats_consumers(machine_list):
    from time import sleep
    print_centralized(' Saving docker stats consumer ')
    
    consumer_list = []
    for containers in machine_list:
        if 'consumer' in machine_list[containers].keys():
            for consumer in machine_list[containers]['consumer']:
                print(f'Docker stats consumer {consumer} from node {containers}..')
                consumer_list.append({'node': containers, 'consumer': consumer})
                sleep(1)
    sleep(1)
    
    print_centralized(' End ')
    return consumer_list

def is_experiment_finished(consumer_list = [], msg_per_consumer = 0):
    from pathlib import Path
    print_centralized(' Waiting for the experiment to finish ', fill_in='.')

    app_folder = '/usr/src/app'
    consumer_number = len(consumer_list)
    completed_consumers = []

    while len(completed_consumers) < consumer_number:
        sleep(2)
        for consumer in consumer_list:
            file_name = f'out_{consumer["node"]}_{consumer["consumer"]}'
            cmd_docker = ['docker', f'-H {consumer["node"]}', 'cp', f'{consumer["consumer"]}:{app_folder}/output_consumer', f'/tmp/{file_name}']
            cmd_string = ' '.join([str(item) for item in cmd_docker])
            subprocess.run(cmd_string, shell=True)
            current_count = rawcount(f'/tmp/{file_name}')
            print(f' --- --- Current count: {current_count}', end='\r')
            sleep(1)
            if (current_count == msg_per_consumer) or (current_count == msg_per_consumer + 1):
                tmp_file = Path(f'/tmp/{file_name}')
                tmp_file.unlink(missing_ok = True)
                completed_consumers.append(consumer)
        sleep(2)

def rawcount(filename):
    f = open(filename, 'rb')
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.raw.read

    buf = read_f(buf_size)
    while buf:
        lines += buf.count(b'\n')
        buf = read_f(buf_size)

    f.close
    return lines

if __name__ == '__main__':
    from networkstructure.nodes import get_node_names
    nodes = get_node_names()
    from networkstructure.containers import get_container_structure
    machine_list = get_container_structure(nodes)
    print(get_docker_stats_consumers(machine_list))
