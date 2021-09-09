#!/usr/bin/env python3
import subprocess
import argparse
from time import sleep
from os import getcwd

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--swarm", help="If the containers are in a docker-swarm (instanciated as services) or not (0 or 1)", nargs='?', const=1, type=int, default=1)
# -k 2 -p 1 -c 2
parser.add_argument("-p", "--producer_destinatary", help="Number of *the* kafka container which the produtor will connect to. I.e to connect to kafka_1, the arg is 1", nargs='?', const=1, type=int, default=1)
parser.add_argument("-c", "--consumer_origin", help="Number of *the* kafka container which the consumer will connect to. I.e to connect to kafka_1, the arg is 1", nargs='?', const=1, type=int, default=1)
parser.add_argument("-t", "--topic_name", help="The kafka topic where produtor and consumer will communicate through", nargs='?', const='messages', type=str, default='messages')
parser.add_argument("-n", "--n_times", help="Runs experiment N times (not yet implemented)", nargs='?', const=1, type=int, default=1)
parser.add_argument("-o", "--output_number", help="Number the final output_consumer file. It is mutually excluse (and overwrites) --n_times", nargs='?', const=0, type=int, default=0)
parser.add_argument("-m", "--messages_to_send", help="Amount of messages sent per test iteration (in the thousands) i.e 100 is 100.000 messages (default 1000)", nargs='?', const=1, type=int, default=1)
parser.add_argument("-w", "--wait", help="Waiting time between test iterations (default 10)", nargs='?', const=1, type=int, default=1)

args = parser.parse_args()

ammount_of_messages = (args.messages_to_send * 1000)
number = args.n_times

if not args.output_number == 0:
    number = args.output_number

current_dir = str(getcwd())

if not args.swarm in (0,1):
    print('\n - Invalid value for swarm argument')
    exit() 

for n in range(args.n_times):
    print(f'\n\nStarting iteration {n} ...\n')
    if args.swarm == 1:
        print('Initializing consumer...')
        subprocess.call(f"docker exec -d $(docker ps -q -f name=kafka_python_consumer_1) bash -c \"python3 kafka_consumer.py -t {args.topic_name} -s kafka_{args.consumer_origin} -p 909{args.consumer_origin} -n {ammount_of_messages}\"", shell=True)
        sleep(5)
        print('Initializing producer...')
        subprocess.call(f"docker exec $(docker ps -q -f name=kafka_python_producer_1) bash -c \"python3 kafka_producer.py -t {args.topic_name} -s kafka_{args.consumer_origin} -p 909{args.producer_destinatary} -n {ammount_of_messages}\"", shell=True) 
        sleep(2)
        print('waiting for file to be written')
        sleep(2)
        subprocess.call(f"docker cp $(docker ps -q -f name=kafka_python_consumer_1):/usr/src/app/output_consumer {current_dir}/output_consumer_{number}", shell=True) 
        print('Extracting the output file "output_consumer"') 

    elif args.swarm == 0:
        print('Initializing consumer...')
        subprocess.run(f"docker exec -d python_consumer_1 bash -c \"python3 kafka_consumer.py -t {args.topic_name} -s kafka_{args.consumer_origin} -p 909{args.consumer_origin} -n {ammount_of_messages}\"", shell=True) 
        sleep(5)
        print('Initializing producer...')
        subprocess.run(f"docker exec python_producer_1 bash -c \"python3 kafka_producer.py -t {args.topic_name} -s kafka_{args.consumer_origin} -p 909{args.producer_destinatary} -n {ammount_of_messages}\"", shell=True) 
        sleep(2)
        print('waiting for file to be written')
        sleep(2)
        subprocess.run(f"docker cp python_consumer_1:/usr/src/app/output_consumer {current_dir}/output_consumer_{number}", shell=True)
        print('Extracting the output file "output_consumer"') 
    
    sleep(args.wait)