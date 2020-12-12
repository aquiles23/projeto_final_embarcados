#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time


def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to MQTT Broker!")
	else:
		print("Failed to connect, return code %d\n", rc)


def temp_message(client, userdata, message):
	pass

def umid_message(client, userdata, message):
	pass

def state_message(client, userdata, message):
	pass

# escolha = int(input("escolha 1 para adicionar novo device\n2 para tananan"))

broker = "mqtt.eclipseprojects.io"

device = "fse2020/160010195/devices/<ID_do_device>"
devi_info = {
	"room": "quarto",
	"in": "interruptor",
	"out": "lampada"
}

client = mqtt.Client("publisher")
client.on_connect = on_connect
client.connect(broker)

if(not client.publish(device, json.dumps(devi_info["room"]), 2)):
	print(f"Failed to send message to topic {device}")

# wait for esp to publish in mqtt?
# time.sleep(1)

temp_topic = f"fse2020/160010195/{devi_info['room']}/temperatura"
umid_topic = f"fse2020/160010195/{devi_info['room']}/umidade"
state_topic = f"fse2020/160010195/{devi_info['room']}/estado"

client.message_callback_add(temp_topic, temp_message)
client.message_callback_add(umid_topic, umid_message)
client.message_callback_add(state_topic, state_message)

client.subscribe(temp_topic)
client.subscribe(umid_topic)
client.subscribe(state_topic)
