#!/usr/bin/env python3
import paho.mqtt.client as mqtt
from threading import Thread
import json
import time
import curses
from room_devices import room_devices


class Mqtt():
	client : mqtt.Client
	def init(self,screen, room:str, matricula="160010195", mac="8c:aa:b5:8b:52:e0"):
		def on_connect(client, userdata, flags, rc):
			if rc == 0:
				pass
			else:
				raise Exception("Failed to connect, return code %d\n", rc)

		def on_publish(client, userdata, mid):
			pass

		def temp_message(client, userdata, message):
			msg = json.loads(message.payload.decode("utf-8"))

		def umid_message(client, userdata, message):
			msg = json.loads(message.payload.decode("utf-8"))

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
			room_devices.esp_in_device({
				room:(
					input_value,
					input_device
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

		self.client = mqtt.Client("publisher")
		self.client.on_connect = on_connect
		self.client.on_publish = on_publish
		self.client.connect(broker)

		if(not self.client.publish(device, json.dumps(room), 2)):
			raise Exception(f"Failed to send message to topic {device}")

		# wait for esp subscribe in mqtt?
		#time.sleep(1)

		temp_topic = f"fse2020/{matricula}/{room}/temperatura"
		umid_topic = f"fse2020/{matricula}/{room}/umidade"
		state_topic = f"fse2020/{matricula}/{room}/estado"

		self.client.message_callback_add(temp_topic, temp_message)
		self.client.message_callback_add(umid_topic, umid_message)
		self.client.message_callback_add(state_topic, state_message)

		self.client.subscribe(temp_topic)
		self.client.subscribe(umid_topic)
		self.client.subscribe(state_topic)

		# program will not shut down
		self.client.loop_forever()

	def run_init(self, *args, **kwargs):
		runner = Thread(target=self.init, daemon = True,args = args)
		runner.start()
		return runner

