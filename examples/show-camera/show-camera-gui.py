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




class Camera:
	
	def __init__(self):
		self.n = 0
		document.bind('click', self.switch)

	def switch(self, e):
		self.n = 1 if self.n == 0 else 0



camera = Camera()


def main():

	photo = termo.app.take_photo(camera.n)
	url = termo.utils.url(termo.utils.blob(photo))
	img.src = url

	window.setTimeout(main, 100)


main()
