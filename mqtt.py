#!/usr/bin/env python3
import paho.mqtt.client as paho_mqtt
from threading import Thread
import json
import time
import curses
from room_devices import room_devices


def mqtt(screen, room:str,y_pos: int, matricula="160010195", mac="8c:aa:b5:8b:52:e0"):
	def on_connect(client, userdata, flags, rc):
		if rc == 0:
			pass
		else:
			raise Exception("Failed to connect, return code %d\n", rc)

	def on_publish(client, userdata, mid):
		pass

	def temp_message(client, userdata, message):
		print("temperatura chegou")
		message = json.loads(message.payload.decode("utf-8"))
		screen.addstr(
			y_pos,
			0,
			f"{message['room']}: temperatura : {message.get('temp')}")

	def umid_message(client, userdata, message):
		message = json.loads(message.payload.decode("utf-8"))
		screen.addstr(
			y_pos+1,
			0,
			f"{message.get('room')}: umidade : {message.get('humidi')}")


	def state_message(client, userdata, message):
		message = json.loads(message.payload.decode("utf-8"))
		room, input_value, output_value = message.values()
		input_device = room_devices.esp_defined_device.get(room).get("in")
		output_device = room_devices.esp_defined_device.get(room).get("out")
		""" room_devices.esp_device.update({
			room:{
				"in": input_value,
				"out": output_value
			}
		}) """
		room_devices.esp_in_device.update({
			room:(
				input_value,
				input_device
			)
		})
		room_devices.esp_out_device.update({
			room:(
				output_value,
				output_device
			)
		})
		room_devices.total_device.update({
			input_device: (
				input_value,
				room
			)
		})
	broker = "mqtt.eclipseprojects.io"

	device = f"fse2020/{matricula}/dispositivos/{mac}"

	client = paho_mqtt.Client(room)
	client.on_connect = on_connect
	client.on_publish = on_publish
	client.connect(broker)
	# client.loop_start()
	# most important message, so i'm using qos 2
	if(not client.publish(device, json.dumps(room),2)):
		raise Exception(f"Failed to send message to topic {device}")

	# wait for esp subscribe in mqtt?
	#time.sleep(1)

	temp_topic = f"fse2020/{matricula}/{room}/temperatura"
	umid_topic = f"fse2020/{matricula}/{room}/umidade"
	state_topic = f"fse2020/{matricula}/{room}/estado"

	client.subscribe(temp_topic)
	client.subscribe(umid_topic)
	client.subscribe(state_topic)

	client.message_callback_add(temp_topic, temp_message)
	client.message_callback_add(umid_topic, umid_message)
	client.message_callback_add(state_topic, state_message)

	room_devices.room_esp.update({room:device})
	# program will not shut down
	client.loop_forever()


	""" def run_init(, *args):
		runner = Thread(target=.init,args = args)
		runner.start()
		return runner """

