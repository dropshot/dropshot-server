import sys, os, bottle

sys.path = ['/var/code/dropshot-server/', '/home/dev/python/bottle/dropshot-server/'] + sys.path

os.chdir(os.path.dirname(__file__))

import dropshot

application = bottle.default_app()

