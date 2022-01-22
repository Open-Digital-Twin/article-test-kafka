# python 3.6

import random
import time

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
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()