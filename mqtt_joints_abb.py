import random

from paho.mqtt import client as mqtt_client

from robodk.robolink import *

RDK = Robolink()
robot  = RDK.Item('ABB IRB 1600-6/1.45')

#broker = '188.24.48.213'
broker = '192.168.1.113'
port = 1883
topic = "licenta/jointsabb"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'basti'
password = 'topsecret'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def filtrare (mesaj):
    nc = "{},:'ja "
    for character in nc:
        mesaj = mesaj.replace(character, "")
    j = mesaj.split('"')
    indices = [2, 4, 6, 8, 10, 12]
    print(mesaj)
    extracted_elements = [j[index] for index in indices]
    for i in range(0, len(extracted_elements)):
        extracted_elements[i] = int(extracted_elements[i])
    return extracted_elements

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        mesaj = msg.payload.decode()
        joints = filtrare(mesaj)
        robot.MoveJ(joints)
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()