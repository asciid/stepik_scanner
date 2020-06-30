#!/usr/bin/env python3

from bs4 import BeautifulSoup
from math import ceil, floor
import termcolor
import requests
import sys
import os


def get_position():

	"""
	Taking last scanning position from file.
	Now with some errors handling!
	"""

	if os.path.exists(posn_file):
		f = open(posn_file, 'r')
		content = f.readlines()
		if len(content) == 0:
			if os_name != 'nt':
				err = termcolor.colored('Поздравляю! Вы затёрли файл с позицией.\nСканируйте заново. Так держать!', 'red')
			else:
				err = 'Поздравляю! Вы затёрли файл с позицией.\nСканируйте заново. Так держать!'
			os.remove(posn_file)
			os.remove(scan_file)
			sys.exit(err)
		elif content[0] in ('\n', '', ' ',):
			os.remove(scan_file)
			position = 1
		else:
			position = int(content[-1][:-1])
		f.close()
	else:
		position = 1

	return position	

def get_status(response):

	"""
	Checking out whether it's 404, 403 or available course.
	"""

	soup = BeautifulSoup(response.text, 'html.parser')

	if response.status_code == 200:
		if soup.title.text == 'Stepik > 404':
			return 404
		elif soup.title.text == '\n  Stepik\n':
			return 403
		else:
			return 200
	else:
		return 404

def get_title(response):

	"""
	Getting a title from html's <title> tag.
	"""

	soup = BeautifulSoup(response.text, 'html.parser')

	if soup.title.text[3:-7] == 'Stepik':
		return ""
	else:
		return soup.title.text[3:-10]

URL = "https://stepik.org/course/"
scan_file = "stepik_courses.txt"
posn_file = ".position"  
position = get_position()
file = open(scan_file, 'a')
posn = open(posn_file, 'w')
system = os.name
banner = """      _             _ _ 
  ___| |_ ___ _ __ (_) | __     _ __   __ _ _ __ ___  ___ _ __ _ __  _   _ 
 / __| __/ _ \ '_ \| | |/ /    | '_ \ / _` | '__/ __|/ _ \ '__| '_ \| | | |
 \__ \ ||  __/ |_) | |   <     | |_) | (_| | |  \__ \  __/ | _| |_) | |_| |
 |___/\__\___| .__/|_|_|\_\____| .__/ \__,_|_|  |___/\___|_|(_) .__/ \__, |
             |_|         |_____|_|                            |_|    |___/
"""

if position == 1: print(banner)

while True:
	try:
		link = URL + str(position)
		r = requests.get(link)
		s = get_status(r)
		
		terminal = os.get_terminal_size()

		if s == 200:
			title = get_title(r)

			if system == 'nt': status = 'GET'
			else: status = termcolor.colored('GET', 'green')

			# This code prints course's title in the center. Not a shitcode actually.
			spaces = (terminal.columns - len(link) - len(title) - 5) / 2
			print(link, floor(spaces) * ' ', title, ceil(spaces) * ' ', '[', status, ']', sep='')

			file.write(link + ' ' + title + ' ' + '\n')
		else:
			if system == 'nt': status = s
			else: status = termcolor.colored(s, 'red')
			print(link.ljust(terminal.columns - 5), '[', status, ']', sep='')

		position += 1

	except KeyboardInterrupt:

		if system == 'nt': exit = '\n[ Завершение работы ]'
		else: exit = termcolor.colored('\n[ Завершение работы ]', 'red') 

		posn.write('%d\n' % position)

		posn.close()
		file.close()

		sys.exit(exit)
