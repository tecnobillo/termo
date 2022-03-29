#!/usr/bin/python3

import sys, os

# Adding termo to the path >
path = os.path.abspath(os.path.split(__file__)[0])
for _ in range(2): path = os.path.split(path)[0]
sys.path.append(path)
# < Adding termo to the path

import pymsgbox
import termo


@termo.app(__file__, gui='show-toast-gui.py')

class AppBackend:

    def show_toast(self, text):

        if os.name == 'posix' and os.environ.get('PREFIX') and 'com.termux' in os.environ['PREFIX']:
        
            os.system(f'termux-toast "{text}"')

        elif os.name == 'posix':
        
            os.system(f'notify-send "{text}"')
        
        elif os.name == 'nt':
        
            pymsgbox.alert(text)
