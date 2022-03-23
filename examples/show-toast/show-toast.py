#!/usr/bin/python3

import os; os.chdir(os.path.split(__file__)[0])
import sys; sys.path.append('../../')

# The above is only necessary because termo is not in the python path
# To use termux-toast install Termux:API (android) and 'pkg install termux-api' (termux=

import termo

@termo.app(__file__, gui='show-toast-gui.py')
class AppBackend:
    def show_toast(self, text):
        os.system(f'termux-toast "{text}"')
