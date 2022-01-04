from subprocess import run, Popen, PIPE
from os import get_terminal_size
from json import dumps

line_width = get_terminal_size().columns
half_line = int(line_width/2)

def get_container_structure(node_name_list = [], exp_num = 0, home_dir = '/home/adbarros/'):
    print('\n' + '-' * (half_line - 14) + ' Getting container structure ' + '-' * (half_line - 15) + '\n')
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

    print('\n' + '-' * (half_line - 2) + ' End ' + '-' * (half_line - 3) + '\n')
    return container_dict

if __name__ == '__main__':
    import nodes
    node_list = nodes.get_node_names()
    get_container_structure(node_list)
