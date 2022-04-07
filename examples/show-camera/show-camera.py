#!/usr/bin/python3

import sys, os

# Adding termo to the path >
path = os.path.abspath(os.path.split(__file__)[0])
for _ in range(2): path = os.path.split(path)[0]
sys.path.append(path)
# < Adding termo to the path

import termo


@termo.app(__file__, gui='show-camera-gui.py', brython_conf=dict(cdn=True, stdlib=True))
class App:

    c = 0

    def get_c(self):
        return self.c

    def take_photo(self, camera):

        temp_file = 'temp.jpg'

        os.system(f'termux-camera-photo -c {camera} {temp_file}') # requires android.permission.CAMERA

        with open(temp_file, 'rb') as f:
            data = f.read()

        os.remove(temp_file)

        self.c += 1

        return data
