#!/usr/bin/env python3
from sensor import sensor
from room_devices import RoomDevices
from mqtt import mqtt
import threading
import curses
import time


def salutation(screen):
	screen.addstr(0, 0, "digite 0 para sair do programa")
	screen.addstr(1, 0, "digite 1 para adicionar um novo dispositivo")
	screen.addstr(2, 0, "digite 2 para setar o estado de um dispositivo")
	screen.addstr(3, 0, "digite 3 para parar o alarme")


def input_str(screen, y_pos : int, lenght : int, instructions = "") -> str:
	screen.clear()
	screen.nodelay(False)
	curses.echo()
	screen.addstr(y_pos - 1, 0, instructions)
	screen.refresh()
	string = screen.getstr(y_pos, 0, lenght)
	curses.noecho()
	screen.nodelay(True)
	return string.decode("utf-8")


if __name__ == "__main__":
	try:
		room_devices = RoomDevices()
		polling = room_devices.run_polling()
		screen = curses.initscr()
		curses.noecho()
		screen.nodelay(True)
		flag = -1
		while flag != ord("0"):
			
			screen.clear()
			salutation(screen)
			room_devices.print_device(screen)

			temp, hum = sensor()
			screen.addstr(4, 0, f"cômodo central. Humidade: {hum} Temperatura {temp}")

			if(flag == ord("1")):
				room = input_str(screen,2,50,"digite o nome do cômodo")
				input_device = input_str(screen,2,50,"digite o nome do dispositivo de entrada")
				output_device = input_str(screen,2,50,"digite o nome do dispositivo de saída")
				room_devices.esp_defined_device.update({
					room : {
						"in": input_device,
						"out": output_device 
					}
				})
				flag_device = input_str(screen,2,1,"digite 1 para definir o dispositivo ou 0 para usar o padrão")
				if(int(flag_device)):
					matricula = input_str(screen,2,1,"digite a matricula")
					mac = input_str(screen,2,1,"digite o endereço mac")
					threading.Thread(target=mqtt, args=(room_devices,screen,matricula,mac), daemon=True)
				else:
					threading.Thread(target=mqtt, args=(room_devices, screen), daemon=True)


			elif (flag == ord("2")):
				room_name = input_str(screen, 2, 50, "digite o nome do cômodo")
				state = bool(
					int(
						input_str(
							screen,
							2,
							1,
							"digite seu estado(1 ou 0)")))
				room_devices.device_set(room_name, state)
				
			elif (flag == ord("3")):
				screen.clear()
				try:
					room_devices.alarm_handle.terminate()
					screen.addstr(6, 0, "alarme desligado")
				except AttributeError:
					screen.addstr(6, 0, "alarme não foi inicializado")
			flag = screen.getch()

			time.sleep(1)

	except Exception as err:
		curses.endwin()
		try:
			# dealocating memory
			room_devices.alarm_handle.close()
		except:
			pass
		# it's easier to debug raising the error
		raise err

	curses.endwin()
	try:
		# dealocating memory
		room_devices.alarm_handle.close()
	except:
		pass