import subprocess
from auxiliaryfunctions.terminal import print_centralized

def save_docker_stats_kafkas(kafka_dict = {}, exp_number = 0, home_dir = '/home/adbarros', exp_type = 'kafka'):
    print_centralized(' Saving docker stats kafkas ')

    file_list = []
    for key in kafka_dict.keys():
        kafka_dict[key].kill()
        stats_stdout , stats_stderr = kafka_dict[key].communicate()
        file_name = f'docker_stats_{key}.txt'
        file_list.append(file_name)
        with open(f'{home_dir}/{exp_type}_experiment_{exp_number}/csv/{file_name}', 'w+') as f:
            f.write(stats_stdout)

    print_centralized(' End ')
    return file_list

def get_docker_stats_nodes(machine_list = '', exp_type = 'kafka'):

    print_centralized(' Getting stats kafkas ')
    
    kafka_list = []
    kafka_dict = {}
    for machine in machine_list:
        if (exp_type in machine_list[machine].keys()):
            for kafka in machine_list[machine][exp_type]:
                ##Collecting kafka container stats
                kafka_dict[kafka] = 0
                cmd_docker = ['docker', f'-H {machine}', 'stats', kafka , '--format', '"{{.Container}}, {{.CPUPerc}}, {{.MemUsage}}, {{.NetIO}}"']
                kafka_dict[kafka] = subprocess.Popen(cmd_docker, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize= 10000000, universal_newlines=True)
                
                print(f'Getting docker stats kafka {kafka} from node {machine}..')
                kafka_list.append({'node': machine, exp_type: kafka})

    print_centralized(' End ')
    return kafka_dict

if __name__ == "__main__":
    from networkstructure.nodes import get_node_names
    nodes = get_node_names()
    from networkstructure.containers import get_container_structure
    container_dict = get_container_structure(nodes)
    dicte = get_docker_stats_nodes(container_dict)
    print(dicte)
