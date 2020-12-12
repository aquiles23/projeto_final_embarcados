#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time
import sys

def mqtt()
	def on_connect(client, userdata, flags, rc):
		if rc == 0:
			pass
		else:
			print("erro ao conectar")
			sys.exit()

	def on_publish(client, userdata, mid):
		pass

	def temp_message(client, userdata, message):
		pass

	def umid_message(client, userdata, message):
		pass

	def state_message(client, userdata, message):
		pass


	# escolha = int(input("escolha 1 para adicionar novo device\n2 para tananan"))

	broker = "mqtt.eclipseprojects.io"

	device = "fse2020/160010195/dispositivos/8c:aa:b5:8b:52:e0"
	devi_info = {
		"room": "quarto",
		"in": "interruptor",
		"out": "lampada"
	}

	client = mqtt.Client("publisher")
	client.on_connect = on_connect
	client.on_publish = on_publish
	client.connect(broker)

	if(not client.publish(device, json.dumps(devi_info["room"]), 2)):
		pass

	# wait for esp subscribe in mqtt?
	#time.sleep(1)

	temp_topic = f"fse2020/160010195/{devi_info['room']}/temperatura"
	umid_topic = f"fse2020/160010195/{devi_info['room']}/umidade"
	state_topic = f"fse2020/160010195/{devi_info['room']}/estado"

	client.message_callback_add(temp_topic, temp_message)
	client.message_callback_add(umid_topic, umid_message)
	client.message_callback_add(state_topic, state_message)

	client.subscribe(temp_topic)
	client.subscribe(umid_topic)
	client.subscribe(state_topic)

	# program will not shut down
	client.loop_forever()
