# python3.6

import random
from sys import exit
from paho.mqtt import client as mqtt_client
import ast
from datetime import datetime
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
buffer_size = args.output_every
n_messages = args.n_messages
# username = 'emqx'
# password = 'public'

message_buffer = []
ammount_of_read_messages = 1
first_message_timestamp = 0

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

def subscribe(client: mqtt_client, redf):
    def on_message(client, userdata, msg):
        global ammount_of_read_messages
        global first_message_timestamp

        message = ast.literal_eval(msg.payload.decode())

        current_time = datetime.timestamp(datetime.now())
        producer_time = message['producer_time']
        value = message['value']
        message_size = objsize.get_deep_size(msg.payload)
        package_size = objsize.get_deep_size(msg)
        topic = msg.topic

        contents = f'{topic},{value},{producer_time},{current_time},{message_size},{package_size}'
        message_buffer.append(contents)

        ammount_of_read_messages += 1

        if len(message_buffer) == buffer_size:
            for item in message_buffer:
                redf.write("%s\n" % item)
            message_buffer.clear()
            print(f'message_number: {ammount_of_read_messages}', end = '\r')
            
        if ammount_of_read_messages == n_messages:
            for item in message_buffer:
                redf.write("%s\n" % item)
            client.disconnect()
            exit()

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    with open('output_mqtt_consumer', 'w', buffering = 1) as redf:
        redf.write('topic,message_value,message_producer_time,message_consumer_time,message_size,total_size\n')
        subscribe(client, redf, qos=1)
        client.loop_forever()
    exit()

if __name__ == '__main__':
    run()