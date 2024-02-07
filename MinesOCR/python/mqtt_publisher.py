# python 3.6

import random
import time
import numpy as np
from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
n_persons_topic = "CoffeeRush/NPersons"
waiting_time_topic = "CoffeeRush/WaitingTime"
data_file_path = "time_estimation_data.npy"
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

def load_data():
    loaded_data = np.load(data_file_path)
    return loaded_data

def save_data(data):
    np.save(data_file_path, data)

def publish(client, n_persons=10, waiting_time=int(load_data().mean())):
    waiting_time *= n_persons

    # result_n_persons = client.publish(n_persons_topic, n_persons)
    # result_waiting_time = client.publish(waiting_time_topic, waiting_time)
    msg = str(waiting_time)+","+str(n_persons)
    result_waiting_time = client.publish(waiting_time_topic, msg)


    # status_n_persons = result_n_persons[0]
    status_waiting_time = result_waiting_time[0]
    # if status_n_persons == 0:
    #     print(f"Send `{n_persons}` to topic `{n_persons_topic}`...")
    # else:
    #     print(f"Failed to send message to topic {n_persons_topic}")
    
    if status_waiting_time == 0:
        print(f"Send `{msg}` to topic `{waiting_time_topic}`...")
    else:
        print(f"Failed to send message to topic {waiting_time_topic}")

def publish_loop(client, n_persons=10):
    while True:
        time.sleep(5)
        publish(client, n_persons)

def run():
    client = connect_mqtt()
    client.loop_start()
    publish_loop(client,12)


if __name__ == '__main__':
    run()
