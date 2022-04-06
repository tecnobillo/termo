#!/usr/bin/python3

import sys, os

# Adding termo to the path >
path = os.path.abspath(os.path.split(__file__)[0])
for _ in range(2): path = os.path.split(path)[0]
sys.path.append(path)
# < Adding termo to the path

import termo

@termo.app(__file__, gui='test-gui.py')
class App:

    def get_text(self):
        return 'José María Sánchez Ruiz'

    def get_data(self):
        return ['á', 1, True, 'é', 1.5, 'ñ']
