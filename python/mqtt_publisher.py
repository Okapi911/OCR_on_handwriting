# python 3.6

import random
import time
import numpy as np
from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
board_image_topic = "MinesOCR/BoardImage"
prediction_topic = "MinesOCR/Prediction"
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


def publish_prediction(client, text='Ielo, Simly Natezl has Jevelayecl inereol;bl Precidary rabol ; tecbnolgy t scite YOur MeJsage exueloges sifh Jeru;ne Ceel Pen zt "s cow (dtely s;ryuishable Frons a hunans hanclritiry: u5 Sinel  Ncted Rnc/ n~; toJey; Ax'):
    result_waiting_time = client.publish(prediction_topic, text)

    status_waiting_time = result_waiting_time[0]
    
    if status_waiting_time == 0:
        print(f"Send `{text}` to topic `{prediction_topic}`...")
    else:
        print(f"Failed to send message to topic {prediction_topic}")


def publish(client, byteArray):
    # file = open(image_path,"rb")
    # fileContent = file.read()
    # byteArray = bytearray(fileContent)
    # file.close()
    result_waiting_time = client.publish(board_image_topic, byteArray)


    status_waiting_time = result_waiting_time[0]
    
    if status_waiting_time == 0:
        print(f"Send `{len(byteArray)}` bytes to topic `{board_image_topic}`...")
    else:
        print(f"Failed to send message to topic {board_image_topic}")

def publish_loop(client, image_path='img/asd.jpeg'):
    while True:
        time.sleep(5)
        # publish(client)
        publish_prediction(client)

def run():
    client = connect_mqtt()
    client.loop_start()
    # publish(client)
    publish_loop(client)


if __name__ == '__main__':
    run()