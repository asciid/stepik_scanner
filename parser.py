#!/usr/bin/env python3

from bs4 import BeautifulSoup
from math import ceil, floor
import termcolor
import requests
import os

def get_position(pose_file, parse_file):

	# Function gets current scan's position.
	# Number is stored in .stepik_scan file in working directory of the script.
	# If (accidently) file is empty, function deletes your scanned links because script has to point to scan.

	if os.path.exists(pose_file):
		f = open(pose_file, 'r')
		content = f.readlines()
		if content[0] in ('\n', '', ' '):
			os.remove(parse_file)
			position = 1
		else:
			position = int(content[-1])
		f.close()
	else:
		position = 1

	return position	

def get_status(response):

	# Stepik's server doesn't anwser 403 on forbidden page. It gives wrapped 403 page but response is 200.
	# All existing cources have a header so the function is about to get this one.

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

	# Function gets course's title. On the site's html it is stored in title:
	# So we have to parse it by hands

	soup = BeautifulSoup(response.text, 'html.parser')

	if soup.title.text[3:-7] == 'Stepik':
		return ""
	else:
		return soup.title.text[3:-10]

URL = "https://stepik.org/course/"
scan_file = "stepik_parse.txt"
posn_file = ".stepik_scan"  
position = get_position(posn_file, scan_file)
file = open(scan_file, 'a')
posn = open(posn_file, 'w')

banner = """
#############################################################################
# ___| |_ ___ _ __ (_) | __     _ __   __ _ _ __ ___  ___ _ __ _ __  _   _  #
#/ __| __/ _ \ '_ \| | |/ /    | '_ \ / _` | '__/ __|/ _ \ '__| '_ \| | | | #
#\__ \ ||  __/ |_) | |   <     | |_) | (_| | |  \__ \  __/ | _| |_) | |_| | #
#|___/\__\___| .__/|_|_|\_\____| .__/ \__,_|_|  |___/\___|_|(_) .__/ \__, | #
#            |_|         |_____|_|                            |_|    |___/  #
#############################################################################"""

print(banner)

while True:
	try:
		link = URL + str(position)
		r = requests.get(link)
		s = get_status(r)
		
		terminal = os.get_terminal_size()

		if s == 200:
			title = get_title(r)

			status = termcolor.colored('GET', 'green')

			# This code prints course's title in the center. Not a shitcode actually.
			spaces = (terminal.columns - len(link) - len(title) - 5) / 2
			print(link, floor(spaces) * ' ', title, ceil(spaces) * ' ', '[', status, ']', sep='')

			file.write(link + ' ' + title + ' ' + '\n')
		else:
			status = termcolor.colored(s, 'red')
			print(link.ljust(terminal.columns - 5), '[', status, ']', sep='')
		
		position += 1

	except KeyboardInterrupt:

		# <Ctrl> + <C> handler

		termcolor.cprint('Завершение', 'red')

		posn.write('%d\n' % position)
		posn.close()
		file.close()

		exit(0)
