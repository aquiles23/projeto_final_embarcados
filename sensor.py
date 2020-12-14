import smbus2
import bme280
import time

def sensor():

	porta_i2c = 1
	endereco = 0x76

	bus = smbus2.SMBus(porta_i2c)
	calibracao_paramentros = bme280.load_calibration_params(bus, endereco)

	dado = bme280.sample(bus, endereco, calibracao_paramentros)
	temp = round(dado.temperature,2)
	hum = round(dado.humidity,  2)
	return (temp,hum)

