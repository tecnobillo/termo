import os; os.chdir(os.path.split(__file__)[0])
import sys; sys.path.append('../../')

import termo
import subprocess


@termo.app(__file__, gui='hello-gui.py')
class AppBackend:

    def get_user(self):
        s = subprocess.run('whoami', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return s.stdout.decode('utf-8').rstrip()