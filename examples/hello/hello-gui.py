import termo
from browser import document
from browser.html import H1

termux_user = termo.app.get_user()

document <= H1(f'Hello {termux_user}!')
