import RPi.GPIO as GPIO
import time

class RoomDevices():
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		self.out = [17, 18] 
		self.inn = [25, 26, 5, 6, 12, 16]
		self.gpio_device = {
			"cozinha": (17, "lampada_1"),
			"sala": (18, "lampada_2")
		}
		GPIO.setup(self.inn, GPIO.IN)
		GPIO.setup(self.out, GPIO.OUT)

	def polling(self):
		pass

	def print_device(self,screen):
		# dict compreension
		total_device = {k:(GPIO.input(v), z) for k, (v, z) in self.gpio_device.items() }
		for enum, (room, (value, device)) in enumerate(total_device.items()):
			screen.addstr(enum, 60, f"comodo: {room}; dispositivo: {device}; estado: {value}")

	def device_set(self,name,state: bool):
		if name in self.gpio_device:
			GPIO.output(self.gpio_device[name][0], state)
			with open("log.csv", "a") as fp:
					fp.write(f"\noutput, {name}, {self.gpio_device[name][1]}, {state}")
