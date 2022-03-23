#!/usr/bin/python3

import os; os.chdir(os.path.split(__file__)[0])
import sys; sys.path.append('../../')

# The above is only necessary because termo is not in the python path
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
