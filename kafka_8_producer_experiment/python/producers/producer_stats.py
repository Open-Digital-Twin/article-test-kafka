from os import get_terminal_size

line_width = get_terminal_size().columns

def get_docker_stats_producers(machine_list):
    print('\n' + '-' * (int(line_width/2) - 10) + ' Getting stats producers ' + '-' * (int(line_width/2) - 10) + '\n')
    
    producer_list = []
    for containers in machine_list:
        if 'producer' in machine_list[containers].keys():
            for producer in machine_list[containers]['producer']:
                print(f'Getting docker stats producer {producer} from node {containers}..')
                producer_list.append({'node': containers, 'producer': producer})

    print('\n' + '-' * (int(line_width/2) - 2) + ' End ' + '-' * (int(line_width/2) - 3) + '\n')
    return producer_list

if __name__ == "__main__":
    from get_all_nodes_names import get_node_names
    nodes = get_node_names()
    from get_container_ids import get_container_structure
    container_dict = get_container_structure(nodes)
    print(get_stats_producers(container_dict))
    
