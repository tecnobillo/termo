#!/usr/bin/python3

import sys, os

# Adding termo to the path >
path = os.path.abspath(os.path.split(__file__)[0])
for _ in range(2): path = os.path.split(path)[0]
sys.path.append(path)
# < Adding termo to the path

import termo

@termo.app(__file__, gui='hello-gui.py', webapp=True, port=5555, title='Termo WebApp')
class AppBackend:
    def get_user(self):
        return os.getlogin()
