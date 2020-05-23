from math import ceil, floor
import requests
import termcolor
import os

def get_position(filename):

	if os.path.exists(filename):
		f = open(filename, 'r')
		content = f.readlines()
		position = int(content[-1])
		f.close()
	else:
		position = 1

	return position	
def get_status(response):

	if response.status_code == 200:
		if response.text.find('<section class="course-promo__head">') != -1:
			return 200
		else:
			return 'ERR'
	else:
		return 404
def get_title(response):

	mark_l = '<h1 class="course-promo__header">'
	mark_r = '</h1>'

	title_l = response.text.find(mark_l) + len(mark_l)
	title_r = response.text.rfind(mark_r)

	return(response.text[title_l:title_r])

URL       = "https://stepik.org/course/"
scan_file = "stepik_parse.txt"
posn_file = ".stepik_scan"  
position  = get_position(posn_file)
file      = open(scan_file, 'a')
posn      = open(posn_file, 'w')

while True:
	try:
		link  = URL + str(position)
		r     = requests.get(link)
		s     = get_status(r)
		title = get_title(r)

		terminal = os.get_terminal_size()

		if s == 200:
			status = termcolor.colored('GET', 'green')
			spaces = (terminal.columns - len(link) - len(title) - 5) / 2
			print(link, floor(spaces) * ' ', title, ceil(spaces) * ' ', '[', status, ']', sep='')
			file.write(link + ' ' + title + ' ' + '\n')
		else:
			status = termcolor.colored(s, 'red')
			print(link.ljust(terminal.columns - 5), '[', status, ']', sep='')
		
		position += 1

	except KeyboardInterrupt:
		termcolor.cprint('Завершение', 'red')

		posn.write('%d\n' % position)
		posn.close()
		file.close()

		exit(0)
		