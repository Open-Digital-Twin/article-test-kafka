# python 3.6

from datetime import datetime
import random
from time import sleep
from paho.mqtt import client as mqtt_client

import argparse
import objsize

parser = argparse.ArgumentParser()

parser.add_argument("-t", "--topic", help="mqtt topic to send the messages", nargs='?', const='topic', type=str, default='topic')
parser.add_argument("-s", "--server", help="mqtt container to connect", nargs='?', const='experiment_mqtt', type=str, default='experiment_mqtt')
parser.add_argument("-p", "--server_port", help="Port where the mqtt container listens", nargs='?', const=1883, type=int, default=1883)
parser.add_argument("-d", "--delay", help="Waiting time beetween messages", nargs='?', const=0.0001, type=float, default=0.0001)
parser.add_argument("-n", "--n_messages", help="Sends N messages", nargs='?', const=1000, type=int, default=1000)
parser.add_argument("-e", "--entries", help="Entries additional to the original dictionary (makes the message bigger)", nargs='?', const=0, type=int, default=0)

args = parser.parse_args()

topic = args.topic
broker = args.server
port = args.server_port
number_of_messages = args.n_messages
delay = args.delay
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    client = mqtt_client.Client(client_id)
    client.connect(broker, port)
    return client

extra_payload = ''
if args.entries > 0:
    for ammount in range(args.entries):
        extra_payload = extra_payload + 'qwertyuiopçlkjhgf'

def publish(client):
    msg_count = 0
    for msg_count in range(number_of_messages):
        sleep(delay)
        msg = str({
            'value': random.randint(100,999), 
            'producer_time': datetime.timestamp(datetime.now()),
            'extra_load': extra_payload
        })
        client.publish(topic, msg)
        if msg_count % 100 == 0:
            print(f'Progress: {msg_count} out of {number_of_messages}', '\r')


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()