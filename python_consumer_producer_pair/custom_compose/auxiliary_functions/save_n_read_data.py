from docker_stats_reader.csv_reader import save_stats_graph

def save_docker_stats(iteration_code, stats_stdout, current_dir):
    print('Saving docker_stats output...')
    with open(f'stats_kafka_{iteration_code}.txt', 'w') as f:
        f.write(stats_stdout)
    print('Generating graphs..')
    save_stats_graph(current_dir, f'stats_kafka_{iteration_code}.txt', f'stats_kafka_{iteration_code}.png', False)
    save_stats_graph(current_dir, f'stats_kafka_{iteration_code}.txt', f'stats_kafka_{iteration_code}_free_scales.png', True)

def container_stats_target(machine, container):
    import subprocess
    container = subprocess.Popen(['docker', '-H', machine, 'ps', '-q', '-f', f'name={container}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    container_stdout, container_stderr = container.communicate()
    return container_stdout.replace('\n','')