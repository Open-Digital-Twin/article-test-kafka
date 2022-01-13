# python3.6

import random

from paho.mqtt import client as mqtt_client

import argparse
import objsize
parser = argparse.ArgumentParser()

parser.add_argument("-t", "--topic", help="mqtt topic to get the messages", nargs='?', const='topic', type=str, default='topic')
parser.add_argument("-s", "--server", help="mqtt container to connect", nargs='?', const='experiment_mqtt', type=str, default='experiment_mqtt')
parser.add_argument("-p", "--server_port", help="Port where the mqtt container listens", nargs='?', const=1883, type=int, default=1883)
parser.add_argument("-n", "--n_messages", help="Sends N messages", nargs='?', const=1000, type=int, default=1000)
parser.add_argument("-o", "--output_every", help="Outputs to file every X messages received, and at the end", nargs='?', const=100, type=int, default=100)

args = parser.parse_args()

topic = args.topic
broker = args.server
port = args.server_port
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
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


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()