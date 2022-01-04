from auxiliaryfunctions.terminal import print_centralized

def get_docker_stats_producers(machine_list):
    print_centralized(' Getting stats producers ')
    
    producer_list = []
    for containers in machine_list:
        if 'producer' in machine_list[containers].keys():
            for producer in machine_list[containers]['producer']:
                print(f'Getting docker stats producer {producer} from node {containers}..')
                producer_list.append({'node': containers, 'producer': producer})

    print_centralized(' End ')
    return producer_list

if __name__ == "__main__":
    from networkstructure.nodes import get_node_names
    nodes = get_node_names()
    from networkstructure.containers import get_container_structure
    container_dict = get_container_structure(nodes)
    print(get_docker_stats_producers(container_dict))
    
