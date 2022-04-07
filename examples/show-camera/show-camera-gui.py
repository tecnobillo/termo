import sys
from browser import alert

class Err:
	def write(self, err):
		alert(err)

sys.stderr = Err()

import termo
from browser import document, window
from browser.html import *

document <= STYLE('''

* {
	margin: 0px;
	padding: 0px;
	box-sizing: border-box;
	background-color: black;
}

body {
	width: 100vw;
	height: 100vh;
	display: flex;
	justify-content: center;
	align-items: center
}

''')

img = IMG(src='', style=dict(
	display='inline-block',
	maxWidth='100%',
	maxHeight='100%'
	))

document <= img



camera = 0

def switch_camera(e):

	global camera

	if camera == 0:
		camera = 1
	elif camera == 1:
		camera = 0


document.bind('click', switch_camera)



c = 0

def main():

	global c

	if c == termo.app.get_c():

		photo = termo.app.take_photo(camera)
		url = termo.utils.url(termo.utils.blob(photo))
		img.src = url
		c += 1

	window.setTimeout(main, 100)


main()
