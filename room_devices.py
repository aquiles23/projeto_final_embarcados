import RPi.GPIO as GPIO
import time
from multiprocessing import Process, Pipe
import subprocess

class RoomDevices():
	alarm_handle : subprocess.Popen
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		self.out = [17, 18] 
		self.inn = [25, 26, 5, 6, 12, 16]
		self.gpio_in_device = {
			"sala": (25, "sensor_presenca_1"),
			"cozinha": (26, "sensor_presenca_2"),
			"porta_cozinha": (5, "sensor_abertura_1"),
			"janela_cozinha": (6, "sensor_abertura_2"),
			"porta_sala": (12, "sensor_abertura_3"),
			"janela_sala": (16, "sensor_abertura_4")

		}
		self.gpio_out_device = {
			"cozinha": (17, "lampada_1"),
			"sala": (18, "lampada_2")
		}
		GPIO.setup(self.inn, GPIO.IN)
		GPIO.setup(self.out, GPIO.OUT)

	def polling(self):
		while(True):
			for room,(pin, device) in self.gpio_in_device.items():
				if GPIO.input(pin):
					with open("log.csv", "a") as fp:
						fp.write(f"\nalarm, {room}, {device}, 1")
			time.sleep(0.5)

	def print_device(self,screen):
		# dict compreension
		total_device = {k:(GPIO.input(v), z) for k, (v, z) in self.gpio_out_device.items() }
		for enum, (room, (value, device)) in enumerate(total_device.items()):
			screen.addstr(enum, 60, f"comodo: {room}; dispositivo: {device}; estado: {value}")

	def device_set(self,name,state: bool):
		if name in self.gpio_out_device:
			GPIO.output(self.gpio_out_device[name][0], state)
			with open("log.csv", "a") as fp:
				fp.write(f"\noutput, {name}, {self.gpio_out_device[name][1]}, {state}")

	def run(self):
		p = Pipe()
		polling = Process(target=self.polling)
		polling.start()
		return polling
