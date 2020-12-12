#!/usr/bin/env python3
from sensor import sensor
import curses

screen = curses.initscr()
curses.noecho()
screen.nodelay(True)
flag = -1
while flag != 0:
	screen.clear()
	screen.addstr(0, 0, "digite 0 para sair do programa")
	flag = screen.getch()
	temp, hum = sensor()
	screen.addstr(1, 0, f"comodo central. Humidade: {hum} Temperatura {temp}")

curses.endwin()