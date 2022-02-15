from auxiliaryfunctions.terminal import print_centralized
from subprocess import run, PIPE

def get_node_names():
    print_centralized(' Getting all network nodes ')
    cmd = ['docker', 'node', 'ls']
    
    result = run(cmd, stdout = PIPE, universal_newlines = True)
    
    node_list = result.stdout.split('\n') # First position is the header, second is the main node, which i dont need
    node_list.pop(0)
    node_list.pop()

    node_name_list = []
    for node in node_list:
        node_line = node.split(' ')
        temp_node = node_line[5]
        if temp_node == '': temp_node = node_line[6]
        node_name_list.append(temp_node)

    print(node_name_list)

    print_centralized(' End ')
    return node_name_list

if __name__ == '__main__':
    get_node_names()
