#!/usr/bin/env python3
from sensor import sensor
import curses
import time

screen = curses.initscr()
curses.noecho()
screen.nodelay(True)
flag = -1
while flag != ord("0"):
	screen.clear()
	screen.addstr(0, 0, "digite 0 para sair do programa")
	screen.addstr(1, 0, "digite 1 para adicionar um novo dispositivo")
	screen.addstr(2, 0, "digite 2 para setar o estado de um dispositivo")
	screen.addstr(3, 0, "digite 3 para parar o alarme")

	if(flag == ord("1")):
		pass
	elif (flag == ord("2")):
		pass
	elif (flag == ord("3")):
		pass	

	temp, hum = sensor()
	screen.addstr(4, 0, f"comodo central. Humidade: {hum} Temperatura {temp}")
	flag = screen.getch()
	time.sleep(0.3)

curses.endwin()