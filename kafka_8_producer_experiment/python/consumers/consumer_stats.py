from os import get_terminal_size

line_width = get_terminal_size().columns

def get_docker_stats_consumers(machine_list):
    from time import sleep
    print('\n' + '-' * (int(line_width/2) - 9) + ' Saving docker stats consumer ' + '-' * (int(line_width/2 - 10)) + '\n')
    
    consumer_list = []
    for containers in machine_list:
        if 'consumer' in machine_list[containers].keys():
            for consumer in machine_list[containers]['consumer']:
                print(f'Docker stats consumer {consumer} from node {containers}..')
                consumer_list.append({'node': containers, 'consumer': consumer})
                sleep(2)
    sleep(1)
    
    print('\n' + '-' * (int(line_width/2) - 2) +  ' End ' + '-' * (int(line_width/2) - 3) + '\n')
    return consumer_list

if __name__ == '__main__':
    from get_all_nodes_names import get_node_names
    nodes = get_node_names()
    from get_container_ids import get_container_structure
    machine_list = get_container_structure(nodes)
    print(get_docker_stats_consumers(machine_list))
