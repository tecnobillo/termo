import termo
from browser import document
from browser.html import *

text = termo.app.get_text()

document <= H1(text)

data = termo.app.get_data()

document <= H1(repr(data))
document <= H1(repr([i.__class__.__name__ for i in data]))
