import subprocess
from time import sleep
from auxiliaryfunctions.terminal import print_centralized

def get_docker_stats_consumers(machine_list, exp_type, exp_number, home_dir = '/home/adbarros'):
    from time import sleep
    print_centralized(' Saving docker stats consumer ')
    consumer_stats_dict = {}
    file_list = []
    consumer_list = []
    for containers in machine_list:
        if 'consumer' in machine_list[containers].keys():
            for consumer in machine_list[containers]['consumer']:
                print(f'Docker stats consumer {consumer} from node {containers}..')
                file_name = f'consumer_stats_{consumer}_{containers}.txt'
                file_list.append(file_name)
                consumer_stats_dict[consumer] = 0
                with open(f'{home_dir}/{exp_type}_experiment_{exp_number}/csv/{file_name}', 'w+') as f:
                    cmd_docker = ['docker', f'-H {containers}', 'stats', consumer , '--format', '"{{.Container}}, {{.CPUPerc}}, {{.MemUsage}}, {{.NetIO}}"']
                    consumer_stats_dict[consumer] = subprocess.Popen(cmd_docker, stdout=f, universal_newlines=True)
                print(f'Getting docker stats consumer {consumer} from node {containers}..')
                consumer_list.append({'node': containers, 'consumer': consumer})
    
    print_centralized(' End ')
    return consumer_list, file_list, consumer_stats_dict

def processes_running(consumer_list):
    from subprocess import PIPE

    consumer_list_processes = []
    for consumer in consumer_list:
        cmd_docker = ['docker', f'-H {consumer["node"]}', 'top', consumer["consumer"]]    
        result = subprocess.run(cmd_docker, stdout=PIPE, universal_newlines=True)
        process_list = result.stdout.split('\n') # Each line, after line 0 is a process
        process_list.pop(0)

        consumer_list_processes.append({consumer["consumer"]: len(process_list)})

    return consumer_list_processes



# this function is slower, but can be useful if there is some problem with the experiment, since it opens the file and reads the lines
def old_is_experiment_finished(consumer_list = [], msg_per_consumer = 0):
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
