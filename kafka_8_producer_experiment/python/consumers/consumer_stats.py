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

if __name__ == '__main__':
    from networkstructure.nodes import get_node_names
    nodes = get_node_names()
    from networkstructure.containers import get_container_structure
    machine_list = get_container_structure(nodes)
    print(get_docker_stats_consumers(machine_list))
