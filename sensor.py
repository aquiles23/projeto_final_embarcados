import smbus2
import bme280
from time import *

def sensor():
	porta_i2c = 1
	endereco = 0x76

	bus = smbus2.SMBus(porta_i2c)
	calibracao_paramentros = bme280.load_calibration_params(bus, endereco)

	# timer = 0

	while True:
		dado = bme280.sample(bus, endereco, calibracao_paramentros)
		temp = round(dado.temperature,2)
		hum = round(dado.humidity,2)
		press = round(dado.pressure,2)

		print(f"aquiles T:{temp}")
		print(f"U:{hum} P:{press}")
		sleep(1)
	# timer +=1
'''
print("ID: " + str(dado.id))
print("Data/Hora: " + str(dado.timestamp))
print("Temperatura: " + str(dado.temperature))
print("Umidade: " + str(dado.humidity))
print("Pressão atmosférica: " + str(dado.pressure))

#sleep(1)
mylcd.lcd_clear()
'''
