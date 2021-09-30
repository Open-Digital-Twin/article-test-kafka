#!/usr/bin/env python3
from random import randint
import subprocess
import argparse
from time import sleep
from os import getcwd
import threading
from fileupload.fileupload import gdrive_upload
parser = argparse.ArgumentParser()

parser.add_argument("-s", "--swarm", help="If the containers are in a docker-swarm (instanciated as services) or not (0 or 1)", nargs='?', const=1, type=int, default=1)
# -k 2 -p 1 -c 2
parser.add_argument("-p", "--producer_destinatary", help="Number of *the* kafka container which the produtor will connect to. I.e to connect to kafka_1, the arg is 1", nargs='?', const=1, type=int, default=1)
parser.add_argument("-c", "--consumer_origin", help="Number of *the* kafka container which the consumer will connect to. I.e to connect to kafka_1, the arg is 1", nargs='?', const=1, type=int, default=1)
parser.add_argument("-t", "--topic_name", help="The kafka topic where produtor and consumer will communicate through", nargs='?', const='messages', type=str, default='messages')
parser.add_argument("-n", "--n_times", help="Runs experiment N times", nargs='?', const=1, type=int, default=1)
parser.add_argument("-o", "--output_number", help="Number the final output_consumer file. It is mutually excluse (and overwrites) --n_times", nargs='?', const=0, type=int, default=0)
parser.add_argument("-m", "--messages_to_send", help="Amount of messages sent per test iteration (in the thousands) i.e 100 is 100.000 messages (default 1000)", nargs='?', const=1, type=int, default=1)
parser.add_argument("-w", "--wait", help="Waiting time between test iterations (default 1)", nargs='?', const=1, type=int, default=1)
parser.add_argument("-l", "--latency", help="Waiting time beetween messages", nargs='?', const=0.0001, type=float, default=0.0001)
parser.add_argument("-e", "--entries", help="Entries additional to the original dictionary (makes the message bigger)", nargs='?', const=0, type=int, default=0)
parser.add_argument("-u", "--upload_to_gdrive", help="When 'true', uploads the experiment output file to the google drive (if configurated)", nargs='?', const='false', type=str, default='false')

args = parser.parse_args()

ammount_of_messages = (args.messages_to_send * 1000)
number = args.n_times

if not args.output_number == 0:
    number = args.output_number

current_dir = str(getcwd())

if not args.swarm in (0,1):
    print('\n - Invalid value for swarm argument')
    exit() 

def stats_thread(swarm):
    docker_stats = subprocess.run(['docker stats','kafka_1' ,'--format', '"{{.Container}}, {{.CPUPerc}}, {{.MemUsage}}, {{.NetIO}}"', '>> docker_stats_out'])
    if swarm == 1:
        docker_stats = subprocess.run(['docker stats', '$(docker ps -q -f name=kafka_kafka_1)' , '--format', '"{{.Container}}, {{.CPUPerc}}, {{.MemUsage}}, {{.NetIO}}"', '>> docker_stats_out'],
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
ex_uid = randint(1, 9999)
x = threading.Thread(target=stats_thread, args=(args.swarm,), daemon=True)
list_of_files = ['tar', 'cf']

if args.swarm != 0:
    tar_name = f'swarm_experiment_{ex_uid}.tar'
else:
    tar_name = f'compose_experiment_{ex_uid}.tar'

list_of_files.append(tar_name)


for n in range(args.n_times):
    print(f'\n\nStarting iteration {n+1} ...\n')
    print(f'Experiment uid {ex_uid} ...\n')
    uid = randint(1, 999)
    if args.swarm == 1:
        # container = subprocess.Popen(['docker', '-H', 'dtwins2', 'ps', '-q', '-f', 'name=kafka_kafka_1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        # container_stdout, container_stderr = container.communicate()
        # container_stdout = container_stdout.replace('\n','')
        # docker_stats = subprocess.Popen(['docker', '-H dtwins2', 'stats', container_stdout, '--format', '"{{.Container}}, {{.CPUPerc}}, {{.MemUsage}}, {{.NetIO}}"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        print('Initializing consumer...')
        subprocess.call(f"docker exec -d $(docker ps -q -f name=kafka_python_consumer_1) bash -c \"python3 kafka_consumer.py -t {args.topic_name}_{uid}_{n+1} -s kafka_{args.consumer_origin} -p 909{args.consumer_origin} -n {ammount_of_messages}\"", shell=True)
        sleep(5)
        print('Initializing producer...')
        subprocess.call(f"docker exec $(docker ps -q -f name=kafka_python_producer_1) bash -c \"python3 kafka_producer.py -t {args.topic_name}_{uid}_{n+1} -s kafka_{args.consumer_origin} -p 909{args.producer_destinatary} -n {ammount_of_messages} -d {args.latency} -e {args.entries}\"", shell=True) 
        sleep(2)
        print('waiting for file to be written')
        sleep(3)
        subprocess.call(f"docker cp $(docker ps -q -f name=kafka_python_consumer_1):/usr/src/app/output_consumer {current_dir}/output_consumer_{uid}_{n+1}.txt", shell=True) 
        print('Extracting the output file "output_consumers"') 
        print(f'Extracting the output file to "output_consumer_{uid}_{n+1}.txt"') 
        print(f'Saving graph into "output_consumer_{uid}_{n+1}.png"')
        subprocess.run([f"python3", "output_reader/reader.py", f"-f output_consumer_{uid}_{n+1}.txt", f"-p output_consumer_{uid}_{n+1}.png"]) 
        subprocess.run([f"python3", "output_reader/reader.py", f"-f output_consumer_{uid}_{n+1}.txt", f"-p output_consumer_{uid}_{n+1}_free_scales.png", "-s True"]) 
        subprocess.call(f"docker cp $(docker ps -q -f name=kafka_python_consumer_1):/usr/src/app/output_consumer {current_dir}/output_consumer_{uid}_{n+1}.txt", shell=True) 
        # docker_stats.kill()
        # stats_stdout , stats_stderr = docker_stats.communicate()
        # f = open(f'stats_kafka_{uid}_{n+1}.txt', 'w')
        # f.write(stats_stdout)
        # f.close()
        # list_of_files.append(f'stats_kafka_{uid}_{n+1}.txt')
        list_of_files.append(f'output_consumer_{uid}_{n+1}.txt')
        list_of_files.append(f'output_consumer_{uid}_{n+1}.png')
        list_of_files.append(f'output_consumer_{uid}_{n+1}_free_scales.png')

        print('done!')

    elif args.swarm == 0:
        print('Initializing consumer...')
        subprocess.run(f"docker exec -d python_consumer_1 bash -c \"python3 kafka_consumer.py -t {args.topic_name}_{uid}_{n+1} -s kafka_{args.consumer_origin} -p 909{args.consumer_origin} -n {ammount_of_messages}\"", shell=True) 
        sleep(5)
        print('Initializing producer...')
        subprocess.run(f"docker exec python_producer_1 bash -c \"python3 kafka_producer.py -t {args.topic_name}_{uid}_{n+1} -s kafka_{args.consumer_origin} -p 909{args.producer_destinatary} -n {ammount_of_messages} -d {args.latency} -e {args.entries}\"", shell=True) 
        sleep(1)
        print('Waiting for file to be written')
        sleep(2)
        subprocess.run(f"docker cp python_consumer_1:/usr/src/app/output_consumer {current_dir}/output_consumer_{uid}_{n+1}.txt", shell=True)
        print(f'Extracting the output file to "output_consumer_{uid}_{n+1}.txt"') 
        print(f'Saving graph into "output_consumer_{uid}_{n+1}.png"')
        subprocess.run(f"docker cp python_consumer_1:/usr/src/app/output_consumer {current_dir}/output_consumer_{uid}_{n+1}.txt", shell=True)
        subprocess.run([f"python3", "output_reader/reader.py", f"-f output_consumer_{uid}_{n+1}.txt", f"-p output_consumer_{uid}_{n+1}.png"]) 
        subprocess.run([f"python3", "output_reader/reader.py", f"-f output_consumer_{uid}_{n+1}.txt", f"-p output_consumer_{uid}_{n+1}_free_scales.png", "-s True"]) 


        list_of_files.append(f'output_consumer_{uid}_{n+1}.txt')
        list_of_files.append(f'output_consumer_{uid}_{n+1}.png')
        list_of_files.append(f'output_consumer_{uid}_{n+1}_free_scales.png')

        print(f'done! experiment_{uid}')

    sleep(args.wait)
sleep(2)
print('zipping all iterations into one file..')

experiment_settings = str(args).replace('Namespace','Settings')
with open(f'experiment_{ex_uid}_settings.txt', 'w') as redf:
    redf.write(experiment_settings)
redf.close()
list_of_files.append(f'experiment_{ex_uid}_settings.txt')


print(list_of_files)
subprocess.run(list_of_files)

list_of_files[0] = 'rm'
list_of_files.pop(1)
list_of_files.pop(1)
print(list_of_files)

subprocess.run(list_of_files)

if args.upload_to_gdrive:
    print('Uploading file to google cloud (for now this removes file from the folder)')
    gdrive_upload(path_to_file=tar_name)
    subprocess.run(['rm', tar_name])