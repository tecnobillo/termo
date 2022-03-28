#!/usr/bin/python3

import os; os.chdir(os.path.split(__file__)[0])
import sys; sys.path.append('../../')

# The above is only necessary because termo is not in the python path
# To use termux-toast install Termux:API (android) and 'pkg install termux-api' (termux)

import os
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
