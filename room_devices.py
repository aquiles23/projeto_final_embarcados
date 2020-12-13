import RPi.GPIO as GPIO
import time

class Room_devices():
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


	def device_set(self,name,state: bool):
		if name in self.gpio_device:
			GPIO.output(self.gpio_device[name],state)
			return
