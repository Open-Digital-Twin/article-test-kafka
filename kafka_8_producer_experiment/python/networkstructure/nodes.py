from subprocess import run, Popen, PIPE
from os import get_terminal_size

line_width = get_terminal_size().columns
half_line = int(line_width/2)

def get_node_names():
    print('\n' + '-' * (half_line - 13) + ' Getting all network nodes ' + '-' * (half_line - 14) + '\n')
    cmd = ['docker', 'node', 'ls']
    
    result = run(cmd, stdout=PIPE, universal_newlines=True)
    
    node_list = result.stdout.split('\n') # First position is the header, second is the main node, which i dont need
    node_list.pop(0)
    node_list.pop()

    node_name_list = []
    for node in node_list:
        temp_node = node.split(' ')[5]
        if temp_node == '': temp_node = 'dtwins1'
        node_name_list.append(temp_node)

    print(node_name_list)
    print('\n' + '-' * (half_line - 2) + ' End ' + '-' * (half_line - 3) + '\n')
    return node_name_list

if __name__ == '__main__':
    get_node_names()
