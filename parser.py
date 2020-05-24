from math import ceil, floor
import requests
import termcolor
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
	# Some pages also respond 403 with no 403 in response's status. That's why I put 'ERR' in return instead of strict 403. 

	if response.status_code == 200:
		if response.text.find('<section class="course-promo__head">') != -1:
			return 200
		else:
			return 'ERR'
	else:
		return 404

def get_title(response):

	# Function gets course's title. On the site's html it is caged in:
	# <h1 class="course-promo__header">Title</h1>
	# So we have to parse it by hands

	mark_l = '<h1 class="course-promo__header">'
	mark_r = '</h1>'

	title_l = response.text.find(mark_l) + len(mark_l)
	title_r = response.text.rfind(mark_r)

	return(response.text[title_l:title_r])

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
		title = get_title(r)
		terminal = os.get_terminal_size()

		if s == 200:
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
		