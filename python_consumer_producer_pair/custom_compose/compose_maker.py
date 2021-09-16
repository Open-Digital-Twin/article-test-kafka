#!/usr/bin/env python3
from sys import exit
import argparse

parser = argparse.ArgumentParser()

# -k 2 -p 1 -c 2
parser.add_argument("-k", "--kafka_replicas", help="Number of kafka instances to be created", nargs='?', const=1, type=int, default=1)
parser.add_argument("-p", "--producer_replicas", help="Number of producer instances to be created", nargs='?', const=1, type=int, default=1)
parser.add_argument("-c", "--consumer_replicas", help="Number of consumer instances to be created", nargs='?', const=1, type=int, default=1)

args = parser.parse_args()

number_of_kafka_instances = int(args.kafka_replicas)
number_of_producer_instances = int(args.producer_replicas)
number_of_consumer_instances = int(args.consumer_replicas)

complete_string_to_be_saved_in_the_file = []

version = """
version: '3.5'
services:
"""
kafka = """
  kafka_%N%:
    container_name: kafka_%N%
    hostname: kafka_%N%
    image: confluentinc/cp-kafka:latest
    ports:
      - target: 909%N%
        published: 909%N%
        protocol: tcp
    depends_on:
      - zookeeper
    environment:
      - KAFKA_BROKER_ID=%N%
      - KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
      - KAFKA_ADVERTISED_LISTENERS=INSIDE://kafka_%N%:2909%N%,OUTSIDE://:909%N%
      - KAFKA_LISTENERS=INSIDE://:2909%N%,OUTSIDE://:909%N%
      - KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=INSIDE:PLAINTEXT,OUTSIDE:PLAINTEXT
      - KAFKA_INTER_BROKER_LISTENER_NAME=INSIDE
      - KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1
    networks:
     kafka_net:
    deploy:
      replicas: 1
      placement:    
        constraints:
          - node.labels.name==dtwins2
"""
zookeeper = """
  zookeeper:
    container_name: zookeeper
    hostname: zookeeper
    image: confluentinc/cp-zookeeper:latest
    ports:
      - "2181:2181"
    environment:
      - ZOOKEEPER_CLIENT_PORT=2181
      - ZOOKEEPER_TICK_TIME=2000
    networks:
     kafka_net:
    deploy:
      replicas: 1
      placement:    
        constraints:
          - node.labels.name==dtwins2
"""
producer = """
  python_producer_%N%:
    container_name: python_producer_%N%  
    image: python-kafka:latest
    stdin_open: true
    tty: true
    networks:
     kafka_net:
    deploy:
      replicas: 1
      placement:    
        constraints:
          - node.labels.name==dtwins1
"""
consumer = """
  python_consumer_%N%:
    container_name: python_consumer_%N%  
    image: python-kafka:latest
    stdin_open: true
    tty: true
    networks:
     kafka_net:
    deploy:
      replicas: 1
      placement:    
        constraints:
          - node.labels.name==dtwins1
"""
network = """
networks:
  kafka_net:
   name: kafka_net
"""

complete_string_to_be_saved_in_the_file.append(version)
complete_string_to_be_saved_in_the_file.append(zookeeper)

print(f'\nCreating compose with {number_of_kafka_instances} kafka container(s), {number_of_producer_instances} producer container(s), and {number_of_consumer_instances} consumer container(s)')

for i in range(number_of_kafka_instances):
    complete_string_to_be_saved_in_the_file.append(kafka.replace('%N%', str(i+1)))

for i in range(number_of_producer_instances):
    complete_string_to_be_saved_in_the_file.append(producer.replace('%N%', str(i+1)))

for i in range(number_of_consumer_instances):
    complete_string_to_be_saved_in_the_file.append(consumer.replace('%N%', str(i+1)))

complete_string_to_be_saved_in_the_file.append(network)

f = open('docker-compose.yml', 'w') 
for container_config in complete_string_to_be_saved_in_the_file:
    f.write(container_config)
f.close()

print('\n - docker-compose.yml created')