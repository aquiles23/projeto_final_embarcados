#!/usr/bin/env python3
from sensor import sensor
from room_devices import RoomDevices
import curses
import time


def salutation(screen):
	screen.addstr(0, 0, "digite 0 para sair do programa")
	screen.addstr(1, 0, "digite 1 para adicionar um novo dispositivo")
	screen.addstr(2, 0, "digite 2 para setar o estado de um dispositivo")
	screen.addstr(3, 0, "digite 3 para parar o alarme")

def input_str(screen, y_pos : int, lenght : int, instructions = "") -> str:
	screen.nodelay(False)
	curses.echo()
	screen.addstr(y_pos - 1, 0, instructions)
	screen.refresh()
	string = screen.getstr(y_pos, 0, lenght)
	curses.noecho()
	screen.nodelay(True)
	return string


if __name__ == "__main__":
	try:
		room_devices = RoomDevices()
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
				pass
			elif (flag == ord("2")):
				room_name = input_str(screen, 7, 50,"digite o nome do cômodo")
				state = bool(
					int(
						input_str(
							screen,
							9,
							1,
							"digite seu estado(1 ou 0)")))
				room_name = room_name.decode("utf-8")
				room_devices.device_set(room_name, state)
				with open("log.csv", "a") as fp:
					fp.write(f"\noutput, {room_name}, {state}")
			elif (flag == ord("3")):
				pass
			flag = screen.getch()

			time.sleep(0.3)

	except Exception as err:
		curses.endwin()
		raise err

	curses.endwin()