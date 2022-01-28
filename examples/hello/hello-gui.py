import termo
from browser import document, alert
from browser.html import *

import sys

class Err:
    def write(self, err):
        alert(err)

sys.stderr = Err()

termux_user = termo.app.get_user()

document <= H1(f'Hello {termux_user}!')

alert(f'Hello {termux_user}!')