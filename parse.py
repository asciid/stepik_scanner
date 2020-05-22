# Вынести последнее сканирование числом в отдельный файл

import requests
import termcolor
import os

def get_current_position(filename):

	# https://stepik.org/course/xxx
	#                           ^26

	f = open(filename, 'r')
	content = f.readlines()

	# Если текущая ссылка -- x, то сканировать нужно с x + 1!
	position = int(content[-1][26:]) + 1
	
	f.close()

	return position

filename = "stepik_parse.txt"
URL = "https://stepik.org/course/"

if os.path.exists(filename) == False:
	f = open(filename, 'w')
	position = 1
else:
	f = open(filename, 'a')
	position = get_current_position(filename)

while True:
	try:
		link = URL + str(position)
		r = requests.get(link)

		if r.status_code == 200:
			status = termcolor.colored('GET', 'green')
			f.write(link + '\n')
		else:
			status = termcolor.colored(r.status_code, 'red')

		terminal = os.get_terminal_size()

		print(link.ljust(terminal.columns - 6), '[', status, ']', sep='')

		position += 1

	except KeyboardInterrupt:
		print('Завершение!')
		f.close()
		exit(0)