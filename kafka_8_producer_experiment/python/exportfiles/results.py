from random import randint
from os import get_terminal_size, makedirs
import subprocess
from time import sleep

line_width = get_terminal_size().columns
half_line = int(line_width/2)

def create_experiment_folder(home_dir = '/home/adbarros'):
    exp_number = randint(111111111,999999999)
    exp_folder = f'/experiment_{exp_number}'
    makedirs(f'{home_dir}{exp_folder}', exist_ok = True)
    makedirs(f'{home_dir}{exp_folder}/csv', exist_ok = True)
    makedirs(f'{home_dir}{exp_folder}/graphs', exist_ok = True)
    return exp_number

def export_output_files(consumer_list = [], exp_number = 0, home_dir = '/home/adbarros'):
    print('\n' + '-' * (half_line - 9)+ ' Exporting files ' + '-' * (half_line - 8) + '\n')
    app_folder = '/usr/src/app'
    exp_folder = f'/experiment_{exp_number}'
    output_files = []
    for consumer in consumer_list:
        file_name = f'out_{consumer["node"]}_{consumer["consumer"]}_{exp_number}'
        cmd_docker = ['docker', f'-H {consumer["node"]}', 'cp', f'{consumer["consumer"]}:{app_folder}/output_consumer', f'{home_dir}{exp_folder}/csv/{file_name}']
        cmd_string = ' '.join([str(item) for item in cmd_docker])
        outputing_file = subprocess.run(cmd_string, shell=True)
        sleep(1)
        output_files.append(file_name)
        print(f'From node {consumer["node"]}, copied consumer {consumer["consumer"]} output, of experiment number {exp_number}')

    
    print('\n' + '-' * (half_line - 3) + ' End ' + '-' * (half_line - 2) + '\n')
    return output_files

if __name__ == '__main__':
    from get_all_nodes_names import get_node_names
    node_list = get_node_names()
    from get_container_ids import get_container_structure
    machine_list = get_container_structure(node_list)

    experiment_number = create_experiment_folder()
    from docker_stats_kafkas import get_docker_stats_kafkas, save_docker_stats_kafkas
    kafka_dict = get_docker_stats_kafkas(machine_list)

    from docker_stats_consumers import get_docker_stats_consumers
    consumer_list = get_docker_stats_consumers(machine_list)
    from create_topics import create_topic_per_consumer
    topic_list = create_topic_per_consumer(consumer_list)
    from start_consumers import start_consumers
    start_consumers(topic_list)
   
    sleep(15)

    from docker_stats_producers import get_docker_stats_producers
    producer_list = get_docker_stats_producers(machine_list)
    from start_producers import start_producers
    start_producers(producer_list, topic_list)
    
    sleep(40)

    stats_files = save_docker_stats_kafkas(kafka_dict, experiment_number)
    from graphics.stats_reader import create_stats_graph
    for file_ in stats_files:
        print(f'Getting graph for stats file {file_}')
        create_stats_graph(experiment_number, file_, save_image= f'{file_}.svg')

    output_files = export_output_files(consumer_list, experiment_number)
    from graphics.output_reader import create_message_graph
    for file_ in output_files:
        print(f'Getting graph for output file {file_}')
        create_message_graph(experiment_number, file_, save_image= f'{file_}.svg')

    from export_files.compact_files import tar_experiment_dir
    tar_filepath = tar_experiment_dir(experiment_number)

    from export_files.upload_cloud import gdrive_upload
    gdrive_upload(tar_filepath)
