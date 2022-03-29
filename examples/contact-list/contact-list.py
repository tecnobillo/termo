#!/usr/bin/python3

import sys, os

# Adding termo to the path >
path = os.path.abspath(os.path.split(__file__)[0])
for _ in range(2): path = os.path.split(path)[0]
sys.path.append(path)
# < Adding termo to the path

# This app requires Termux:API and 'pkg install termux-api'
# This app requires permission to read the contact list

import termo
import subprocess
import json


@termo.app(__file__, gui='contact-list-gui.py')

class AppBackend:

	def get_contact_list(self):

		s = subprocess.run('termux-contact-list', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

		return json.loads(s.stdout.decode())
