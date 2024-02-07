# python3.6

import random

from paho.mqtt import client as mqtt_client
from mqtt_publisher import load_data, save_data
import numpy as np


broker = 'broker.emqx.io'
port = 1883
topic = "CoffeeRush/AddWaitingTime"
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
        data = list(load_data())
        data.append( int(msg.payload.decode()))
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        save_data(np.array(data))

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
