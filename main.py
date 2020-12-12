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
	temp, hum = sensor()
	screen.addstr(1, 0, f"comodo central. Humidade: {hum} Temperatura {temp}")
	flag = screen.getch()
	time.sleep(1)

curses.endwin()