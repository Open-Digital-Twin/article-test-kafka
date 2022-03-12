from auxiliaryfunctions.terminal import print_centralized
import subprocess

def get_docker_stats_producers(machine_list, exp_type, exp_number, home_dir = '/home/adbarros'):
    print_centralized(' Getting stats producers ')
    producer_stats_dict = {}
    file_list = []
    producer_list = []
    for containers in machine_list:
        if 'producer' in machine_list[containers].keys():
            for producer in machine_list[containers]['producer']:
                print(f'Getting docker stats producer {producer} from node {containers}..')
                file_name = f'producer_stats_{producer}__{containers}.txt'
                file_list.append(file_name)
                producer_stats_dict[producer] = 0
                with open(f'{home_dir}/{exp_type}_experiment_{exp_number}/csv/{file_name}', 'w+') as f:
                    cmd_docker = ['docker', f'-H {containers}', 'stats', producer , '--format', '"{{.Container}}, {{.CPUPerc}}, {{.MemUsage}}, {{.NetIO}}"']
                    producer_stats_dict[producer] = subprocess.Popen(cmd_docker, stdout=f, universal_newlines=True)
                print(f'Getting docker stats producer {producer} from node {containers}..')
                producer_list.append({'node': containers, 'producer': producer})

    print_centralized(' End ')
    return producer_list, file_list, producer_stats_dict

if __name__ == "__main__":
    from networkstructure.nodes import get_node_names
    nodes = get_node_names()
    from networkstructure.containers import get_container_structure
    container_dict = get_container_structure(nodes)
    print(get_docker_stats_producers(container_dict))
    
