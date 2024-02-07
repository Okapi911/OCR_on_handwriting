# python3.6
import easyocr
import random
import cv2
from paho.mqtt import client as mqtt_client
from mqtt_publisher import load_data, save_data
import numpy as np


reader = easyocr.Reader(['en'])
broker = 'broker.emqx.io'
port = 1883
board_image_topic = "MinesOCR/BoardImage"
prediction_topic = "MinesOCR/Prediction"
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


def subscribe_img_topic(client: mqtt_client):
    def on_message(client, userdata, msg):
        content = msg.payload
        np_arr = np.frombuffer(content, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        results = reader.readtext(image)
        ans = " ".join([res[1] for res in results])
        print(f"Received `{ans}` from `{msg.topic}` topic")

    client.subscribe(board_image_topic)
    client.on_message = on_message

def subscribe_prediction_topic(client: mqtt_client):
    def on_message(client, userdata, msg):
        recognized_text = msg.payload.decode()
        print(f"Received `{recognized_text}` from `{msg.topic}` topic")

    client.subscribe(prediction_topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe_prediction_topic(client)
    client.loop_forever()


if __name__ == '__main__':
    run()