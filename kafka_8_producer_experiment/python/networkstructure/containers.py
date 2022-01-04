from subprocess import run, PIPE
from json import dumps

from auxiliaryfunctions.terminal import print_centralized

def get_container_structure(node_name_list = [], exp_num = 0, home_dir = '/home/adbarros/'):
    print_centralized(' Getting container structure ')

    container_dict = {}
    for node_name in node_name_list:
        cmd = ['docker', '-H', node_name, 'ps']
        result = run(cmd, stdout=PIPE, universal_newlines=True)
        
        container_list = result.stdout.split('\n') # Each line, after line 0 is a container
        container_list.pop(0)
            
        container_name_list = {}
        container_type = 'undefined'
        for container in container_list[:-1]:
            if '_python_consumer' in container:
                container_type = 'consumer'
            elif '_python_producer' in container:
                container_type = 'producer'
            elif ('_kafka' in container):
                container_type = 'kafka'
            elif ('_zookeeper'):
                container_type = 'zookeeper'
            if container_type not in container_name_list.keys():
                container_name_list[container_type] = []
            container_name_list[container_type].append(container.split(' ')[0])
        
        container_dict[node_name] = container_name_list
   
    print(dumps(container_dict, indent= 2, default= str))

    with open(f'{home_dir}experiment_{exp_num}/network_structure.txt','w') as file:
        file.write(dumps(container_dict, indent= 2, default= str))

    print_centralized(' End ')
    return container_dict

if __name__ == '__main__':
    import nodes
    node_list = nodes.get_node_names()
    get_container_structure(node_list)
