import RPi.GPIO as GPIO
import time

class RoomDevices():
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		self.out = [17,18] 
		self.inn = [25,26,5,6,12,16]
		self.gpio_device = {
			"cozinha": 17,
			"sala": 18
		}
		GPIO.setup(self.inn, GPIO.IN)
		GPIO.setup(self.out, GPIO.OUT)

	def polling(self):
		pass

	def print_device(self,screen):
		# dict compreension
		total_device = {k:GPIO.input(v) for k,v in self.gpio_device.items() }
		for x,(y,z) in enumerate(total_device.items()):
			screen.addstr(x,60,f"{y} : {z}")

	def device_set(self,name,state: bool):
		if name in self.gpio_device:
			GPIO.output(self.gpio_device[name],state)
			return
