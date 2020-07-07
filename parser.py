#!/usr/bin/env python3

from bs4 import BeautifulSoup
from math import ceil, floor
import requests
import sys
import os

def get_position():

	if os.path.exists(posn_file):
		with open(posn_file, 'r') as f:
			content = f.readlines()

			if len(content) == 0 or content[0] in ('\n', '', ' ',):

				answer = input('Your position file has been damaned.\nWould you like to state a scanning point by yourself (y/n): ')
				
				if answer.lower() == 'y': 
					position = int(input('Enter the number of a course: '))
				else:
					print('Scan will be started from the beginning.')
					os.remove(scan_file + '.txt')
					
					if os.path.exists(scan_file + '.md'):
						os.remove(scan_file + '.md')

					position = 1
			else:
				position = int(content[-1][:-1])
	else:
		position = 1

	return position	

def get_status(response):

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

	soup = BeautifulSoup(response.text, 'html.parser')

	if soup.title.text[3:-7] == 'Stepik':
		return ""
	else:
		return soup.title.text[3:-10]


# Trick to disable colored output on Windows
if os.name != 'nt':
	from termcolor import colored
else: 
	colored = lambda str, color: str

# Arguments


md_output = False

if len(sys.argv) > 1:
	if sys.argv[1] == '--markdown' or sys.argv[1] == '-m':
		md_output = True
	elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
		msg = """stepik_scanner -- Parser for stepik.org\n
--markdown | -m -- Write in Markdown.
--help     | -h -- Print this message and exit.

ISSUES: <github.com/asciid/stepik_scanner>"""
		sys.exit(msg)

URL = "https://stepik.org/course/"
scan_file = "stepik_courses"
posn_file = ".position"  
position = get_position()
banner = r"""      _             _ _ 
  ___| |_ ___ _ __ (_) | __     _ __   __ _ _ __ ___  ___ _ __ _ __  _   _ 
 / __| __/ _ \ '_ \| | |/ /    | '_ \ / _` | '__/ __|/ _ \ '__| '_ \| | | |
 \__ \ ||  __/ |_) | |   <     | |_) | (_| | |  \__ \  __/ | _| |_) | |_| |
 |___/\__\___| .__/|_|_|\_\____| .__/ \__,_|_|  |___/\___|_|(_) .__/ \__, |
             |_|         |_____|_|                            |_|    |___/
"""

print(banner)

if md_output:
	if not os.path.exists(scan_file + '.md'):
		with open(scan_file + '.md', 'w') as file:
			if position == 1: file.write('# Stepik courses\n---\n')
			file.close()	

while True:
	try:
		link = URL + str(position)
		r = requests.get(link)
		s = get_status(r)
		
		terminal = os.get_terminal_size()

		if s == 200:
			title = get_title(r)
			status = colored('GET', 'green')

			# This code prints course's title in the center. Not a shitcode actually.
			spaces = (terminal.columns - len(link) - len(title) - 5) / 2
			print(link, floor(spaces) * ' ', title, ceil(spaces) * ' ', '[', status, ']', sep='')

			if md_output:
				with open(scan_file + '.md', 'a') as file:
					file.write('1. [{}]({})\n\n'.format(title, link))
			else:
				with open(scan_file + '.txt', 'a') as file:
					file.write(link + ' ' + title + ' ' + '\n')
		else:	
			status = colored(s, 'red')
			print(link.ljust(terminal.columns - 5), '[', status, ']', sep='')

		position += 1

		with open(posn_file, 'w') as posn:
			posn.write('%d\n' % position)

	except :

		exit = colored('\n[ Завершение работы ]', 'red') 
		sys.exit(exit)
