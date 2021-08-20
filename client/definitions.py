import sys
from os.path import abspath, join
HERE = abspath(".")
try:
    BASE_PATH = sys._MEIPASS
except Exception:
    BASE_PATH = abspath(".")

res = (600, 300)

UTF8      = 'utf-8'
PORT_CONN = '5555'
PORT_HAND = '5556'
PORT_SUBS = '5557'
ADDRESS   = 'localhost'
try:
    with open(join(HERE, 'connect_loc.txt'), 'r') as location_file:
        ADDRESS = location_file.read().rstrip()
except: pass

SHOULD_STOP_GAME  = True
MOUSE_RIGHT_CLICK = 3
MOUSE_LEFT_CLICK  = 1

INDIGO = ( 67,  74, 135)
RED    = (255,   0,   0)
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
YELLOW = (255, 255,   0)

PLAYER_WIDTH  = 15
PLAYER_HEIGHT = 30
PLAYER_RENDER_PADDING = 1

CD_DURATION = 0.5

asset = lambda fn : join(BASE_PATH, 'assets', fn)
