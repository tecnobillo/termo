#!/usr/bin/python3

import os; os.chdir(os.path.split(__file__)[0] or '.')
import sys; sys.path.append('../../')

# The above is only necessary because termo is not in the python path

import termo

@termo.app(__file__, gui='hello-gui.py')
class AppBackend:
    def get_user(self):
        return os.getlogin()
