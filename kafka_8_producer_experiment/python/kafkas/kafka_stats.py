from os import get_terminal_size
import subprocess
line_width = get_terminal_size().columns

def save_docker_stats_kafkas(kafka_dict = {}, exp_number = 0, home_dir = '/home/adbarros'):
    
    file_list = []
    for key in kafka_dict.keys():
        kafka_dict[key].kill()
        stats_stdout , stats_stderr = kafka_dict[key].communicate()
        file_name = f'docker_stats_{key}.txt'
        file_list.append(file_name)
        with open(f'{home_dir}/experiment_{exp_number}/csv/{file_name}', 'w+') as f:
            f.write(stats_stdout)

    return file_list

def get_docker_stats_kafkas(machine_list):
    print('\n' + '-' * (int(line_width/2) - 10) + ' Getting stats kafkas ' + '-' * (int(line_width/2) - 10) + '\n')
    
    kafka_list = []
    kafka_dict = {}
    for containers in machine_list:
        if ('kafka' in machine_list[containers].keys()):
            for kafka in machine_list[containers]['kafka']:
                ##Collecting kafka containers stats
                kafka_dict[kafka] = 0
                cmd_docker = ['docker', f'-H {containers}', 'stats', kafka , '--format', '"{{.Container}}, {{.CPUPerc}}, {{.MemUsage}}, {{.NetIO}}"']
                kafka_dict[kafka] = subprocess.Popen(cmd_docker, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                
                print(f'Getting docker stats kafka {kafka} from node {containers}..')
                kafka_list.append({'node': containers, 'kafka': kafka})

    print('\n' + '-' * (int(line_width/2) - 2) + ' End ' + '-' * (int(line_width/2) - 3) + '\n')
    return kafka_dict

if __name__ == "__main__":
    from get_all_nodes_names import get_node_names
    nodes = get_node_names()
    from get_container_ids import get_container_structure
    container_dict = get_container_structure(nodes)
    dicte = get_docker_stats_kafkas(container_dict)
    print(dicte)
