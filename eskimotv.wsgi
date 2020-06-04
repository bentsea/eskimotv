#!/home/eskimotv/eskimoenv/bin/python

activate_this = '/home/eskimotv/eskimoenv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys,os
import logging
logging.basicConfig(stream=sys.stderr)
path = "/home/eskimotv/public_html/"
if path not in sys.path:
    sys.path.append(path)
from eskimotv import app as application
